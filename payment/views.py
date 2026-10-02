from io import BytesIO

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied, ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView
from xhtml2pdf import pisa

from config.shared.access import user_is_manager
from payment.forms import PaymentForm
from payment.models import Payment
from payment.utils.constants import PAYMENTS_PER_PAGE
from payment.utils.services import (
    apply_payment,
    get_transaction_summary,
    get_transactions_summary_batch,
)
from transaction.models import Transaction
from transaction.utils.constants import ContractStatusChoices
from transaction.utils.services import calculate_transaction_cost


class PaymentListView(LoginRequiredMixin, TemplateView):
    template_name = "payment/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Payment.objects.select_related(
            "transaction",
            "transaction__customer",
            "transaction__collateral",
            "transaction__scheme",
            "created_by",
        ).order_by("-tanggal_bayar", "-created_at")
        paginator = Paginator(queryset, PAYMENTS_PER_PAGE)
        page_obj = paginator.get_page(self.request.GET.get("page"))
        trx_ids = [p.transaction_id for p in page_obj.object_list]
        lunas_trx_ids = set(
            Transaction.objects.filter(
                pk__in=trx_ids,
                status_kontrak=ContractStatusChoices.LUNAS,
            ).values_list("pk", flat=True)
        )
        context["page_obj"] = page_obj
        context["total_payments"] = queryset.count()
        context["lunas_trx_ids"] = lunas_trx_ids
        return context


class PaymentChooseView(LoginRequiredMixin, TemplateView):
    template_name = "payment/choose.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = (
            Transaction.objects.filter(
                status_kontrak__in=[
                    ContractStatusChoices.AKTIF,
                    ContractStatusChoices.JATUH_TEMPO,
                ]
            )
            .select_related("customer", "collateral", "scheme")
            .order_by("-tanggal_pinjam", "-created_at")
        )
        trx_list = list(queryset[:100])
        summaries = get_transactions_summary_batch(trx_list)
        items = []
        for trx in trx_list:
            summary = summaries.get(trx.pk)
            if summary and not summary["lunas"]:
                items.append({"trx": trx, "summary": summary})
        context["items"] = items
        context["form_title"] = "Pilih Transaksi untuk Dibayar"
        context["form_subtitle"] = (
            "Ketik untuk mencari transaksi aktif yang perlu dibayar"
        )
        return context


class PaymentCreateView(LoginRequiredMixin, View):
    template_name = "payment/form.html"

    def _get_transaction(self, transaction_pk):
        return get_object_or_404(
            Transaction.objects.select_related(
                "customer",
                "collateral",
                "collateral__category",
                "scheme",
                "storages",
            ),
            pk=transaction_pk,
        )

    def _context(self, trx, form, summary):
        cost = calculate_transaction_cost(trx.uang_pinjaman, trx.scheme)
        return {
            "trx": trx,
            "form": form,
            "summary": summary,
            "cost": cost,
            "sisa_bayar": summary["sisa_bayar"],
            "form_title": "Pembayaran Baru",
            "form_subtitle": f"Kontrak {trx.nomor_kontrak}",
        }

    def get(self, request, transaction_pk):
        trx = self._get_transaction(transaction_pk)
        summary = get_transaction_summary(trx)
        if summary["lunas"]:
            messages.error(request, "Transaksi ini sudah lunas.")
            return redirect("transaction:detail", pk=trx.pk)
        form = PaymentForm()
        return render(request, self.template_name, self._context(trx, form, summary))

    def post(self, request, transaction_pk):
        trx = self._get_transaction(transaction_pk)
        summary = get_transaction_summary(trx)
        if summary["lunas"]:
            messages.error(request, "Transaksi ini sudah lunas.")
            return redirect("transaction:detail", pk=trx.pk)

        form = PaymentForm(request.POST)
        if not form.is_valid():
            messages.error(request, "Periksa kembali data yang Anda masukkan.")
            return render(
                request, self.template_name, self._context(trx, form, summary)
            )

        data = form.cleaned_data
        try:
            payment = apply_payment(
                transaction=trx,
                jumlah_bayar=data["jumlah_bayar"],
                tipe_pembayaran=data["tipe_pembayaran"],
                metode_pembayaran=data["metode_pembayaran"],
                tanggal_bayar=data["tanggal_bayar"],
                created_by=request.user,
                catatan=data.get("catatan", ""),
                nomor_pembayaran=data.get("nomor_pembayaran"),
            )
        except IntegrityError:
            messages.error(
                request,
                "Gagal menyimpan pembayaran. Data mungkin duplikat.",
            )
            return render(
                request, self.template_name, self._context(trx, form, summary)
            )
        except ValidationError as exc:
            messages.error(request, str(exc))
            return render(
                request, self.template_name, self._context(trx, form, summary)
            )
        except Exception as exc:
            messages.error(request, f"Gagal menyimpan pembayaran: {exc}")
            return render(
                request, self.template_name, self._context(trx, form, summary)
            )

        messages.success(
            request,
            f"Pembayaran {payment.nomor_pembayaran} berhasil dicatat.",
        )
        return redirect(f"{reverse('payment:detail', args=[payment.pk])}?print=1")


class PaymentDetailView(LoginRequiredMixin, TemplateView):
    template_name = "payment/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        payment = get_object_or_404(
            Payment.objects.select_related(
                "transaction",
                "transaction__customer",
                "transaction__collateral",
                "transaction__collateral__category",
                "transaction__scheme",
                "transaction__storages",
                "created_by",
            ),
            pk=self.kwargs["pk"],
        )
        context["payment"] = payment
        context["trx"] = payment.transaction
        context["summary"] = get_transaction_summary(payment.transaction)
        context["cost"] = calculate_transaction_cost(
            payment.transaction.uang_pinjaman,
            payment.transaction.scheme,
        )
        context["auto_print"] = self.request.GET.get("print") == "1"
        return context


class PaymentPDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        payment = get_object_or_404(
            Payment.objects.select_related(
                "transaction",
                "transaction__customer",
                "transaction__collateral",
                "transaction__scheme",
                "created_by",
            ),
            pk=pk,
        )
        trx = payment.transaction
        summary = get_transaction_summary(trx)
        cost = calculate_transaction_cost(trx.uang_pinjaman, trx.scheme)

        from core.utils.services import get_brand, get_orgs

        context = {
            "payment": payment,
            "trx": trx,
            "summary": summary,
            "cost": cost,
            "brand": get_brand(),
            "orgs": get_orgs(),
            "generated_at": timezone.now(),
        }
        html = render_to_string("payment/payment/pdf.html", context, request=request)
        result = BytesIO()
        pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), result, encoding="utf-8")
        if pdf.err:
            return HttpResponse("Gagal membuat PDF.", status=500)
        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="Kwitansi-{payment.nomor_pembayaran}.pdf"'
        )
        return response


class PaymentDeleteView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        if not user_is_manager(request.user):
            raise PermissionDenied
        target = get_object_or_404(Payment, pk=pk)
        number = target.nomor_pembayaran
        try:
            target.delete()
        except ProtectedError:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Pembayaran tidak dapat dihapus karena masih digunakan.",
                },
                status=400,
            )
        return JsonResponse(
            {"success": True, "message": f"Pembayaran {number} berhasil dihapus."}
        )
