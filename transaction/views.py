from io import BytesIO

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.db import transaction as db_transaction
from django.db.models import ProtectedError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView, UpdateView
from xhtml2pdf import pisa

from collateral.models import Collateral
from customer.models import Customer
from payment.models import Payment
from payment.utils.services import get_transaction_summary
from transaction.forms import (
    CollateralQuickForm,
    CustomerQuickForm,
    NewTransactionForm,
    TransactionForm,
)
from transaction.models import Transaction
from transaction.utils.constants import TRANSACTIONS_PER_PAGE
from transaction.utils.services import calculate_transaction_cost
from vault.models import Scheme

FORM_TABS = [
    {"id": "nasabah", "label": "Nasabah", "icon": "fa-user"},
    {"id": "collateral", "label": "Barang Jaminan", "icon": "fa-boxes-stacked"},
    {"id": "transaksi", "label": "Rincian Transaksi", "icon": "fa-hand-holding-dollar"},
]


def _get_schemes_data():
    data = {}
    for scheme in Scheme.objects.all():
        data[str(scheme.pk)] = {
            "durasi": scheme.durasi_maksimal_hari,
            "bunga": str(scheme.bunga),
            "biaya_admin": str(scheme.biaya_admin),
        }
    return data


class TransactionListView(LoginRequiredMixin, TemplateView):
    template_name = "transaction/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Transaction.objects.select_related(
            "customer", "collateral", "scheme", "storages", "created_by"
        ).order_by("-tanggal_pinjam", "-created_at")
        paginator = Paginator(queryset, TRANSACTIONS_PER_PAGE)
        page_obj = paginator.get_page(self.request.GET.get("page"))
        context["page_obj"] = page_obj
        context["total_transactions"] = queryset.count()
        return context


class TransactionNewView(LoginRequiredMixin, View):
    template_name = "transaction/trx.html"

    def _base_context(self):
        return {
            "form_tabs": FORM_TABS,
            "schemes_data": _get_schemes_data(),
            "customers": Customer.objects.filter(is_active=True).order_by("name"),
            "collaterals": Collateral.objects.filter(is_active=True)
            .select_related("category")
            .order_by("name"),
            "customer_form": CustomerQuickForm(prefix="cust"),
            "collateral_form": CollateralQuickForm(prefix="coll"),
            "trx_form": NewTransactionForm(prefix="trx"),
            "customer_mode": "new",
            "collateral_mode": "new",
            "form_title": "Transaksi Baru",
            "form_subtitle": "Buat kontrak gadai dengan nasabah baru atau lama",
        }

    def _render_invalid(
        self, customer_form, collateral_form, trx_form, customer_mode, collateral_mode
    ):
        context = self._base_context()
        context["customer_form"] = customer_form
        context["collateral_form"] = collateral_form
        context["trx_form"] = trx_form
        context["customer_mode"] = customer_mode
        context["collateral_mode"] = collateral_mode
        return render(self.request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self._base_context())

    def post(self, request, *args, **kwargs):
        customer_mode = request.POST.get("customer_mode", "new")
        collateral_mode = request.POST.get("collateral_mode", "new")

        customer_form = CustomerQuickForm(request.POST, request.FILES, prefix="cust")
        collateral_form = CollateralQuickForm(
            request.POST, request.FILES, prefix="coll"
        )
        trx_form = NewTransactionForm(request.POST, prefix="trx")

        customer_valid = True
        collateral_valid = True
        existing_customer = None
        existing_collateral = None

        if customer_mode == "existing":
            customer_id = request.POST.get("existing_customer_id")
            if customer_id:
                existing_customer = Customer.objects.filter(
                    pk=customer_id, is_active=True
                ).first()
            if not existing_customer:
                customer_valid = False
                messages.error(request, "Nasabah lama tidak valid atau belum dipilih.")
        else:
            customer_valid = customer_form.is_valid()

        if collateral_mode == "existing":
            collateral_id = request.POST.get("existing_collateral_id")
            if collateral_id:
                existing_collateral = Collateral.objects.filter(
                    pk=collateral_id, is_active=True
                ).first()
            if not existing_collateral:
                collateral_valid = False
                messages.error(request, "Barang lama tidak valid atau belum dipilih.")
        else:
            collateral_valid = collateral_form.is_valid()

        trx_valid = trx_form.is_valid()

        if not (customer_valid and collateral_valid and trx_valid):
            return self._render_invalid(
                customer_form,
                collateral_form,
                trx_form,
                customer_mode,
                collateral_mode,
            )

        try:
            with db_transaction.atomic():
                if customer_mode == "existing":
                    customer = existing_customer
                else:
                    customer = customer_form.save(commit=False)
                    customer.is_active = True
                    customer.save()

                if collateral_mode == "existing":
                    collateral = existing_collateral
                else:
                    collateral = collateral_form.save(commit=False)
                    collateral.status = "stored"
                    collateral.is_active = True
                    collateral.save()

                trx = trx_form.save(commit=False)
                trx.customer = customer
                trx.collateral = collateral
                trx.created_by = request.user
                trx.save()
        except IntegrityError:
            messages.error(
                request,
                "Gagal menyimpan. NIK, kode, atau nomor kontrak mungkin sudah dipakai.",
            )
            return self._render_invalid(
                customer_form,
                collateral_form,
                trx_form,
                customer_mode,
                collateral_mode,
            )
        except ValidationError as exc:
            messages.error(request, f"Data tidak valid: {exc}")
            return self._render_invalid(
                customer_form,
                collateral_form,
                trx_form,
                customer_mode,
                collateral_mode,
            )
        except Exception as exc:
            messages.error(request, f"Gagal membuat transaksi: {exc}")
            return self._render_invalid(
                customer_form,
                collateral_form,
                trx_form,
                customer_mode,
                collateral_mode,
            )

        messages.success(request, f"Transaksi {trx.nomor_kontrak} berhasil dibuat.")
        return redirect("transaction:detail", pk=trx.pk)


class TransactionDetailView(LoginRequiredMixin, TemplateView):
    template_name = "transaction/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trx = get_object_or_404(
            Transaction.objects.select_related(
                "customer",
                "collateral",
                "collateral__category",
                "scheme",
                "storages",
                "created_by",
            ),
            pk=self.kwargs["pk"],
        )
        context["trx"] = trx
        context["cost"] = calculate_transaction_cost(trx.uang_pinjaman, trx.scheme)
        context["payment_summary"] = get_transaction_summary(trx)
        context["payments"] = (
            Payment.objects.filter(transaction=trx)
            .select_related("created_by")
            .order_by("-tanggal_bayar", "-created_at")
        )
        return context


class TransactionPDFView(LoginRequiredMixin, View):
    def get(self, request, pk):
        trx = get_object_or_404(
            Transaction.objects.select_related(
                "customer",
                "collateral",
                "collateral__category",
                "scheme",
                "storages",
                "created_by",
            ),
            pk=pk,
        )
        cost = calculate_transaction_cost(trx.uang_pinjaman, trx.scheme)

        from core.utils.services import get_brand, get_orgs

        context = {
            "trx": trx,
            "cost": cost,
            "brand": get_brand(),
            "orgs": get_orgs(),
            "generated_at": timezone.now(),
        }
        html = render_to_string("transaction/trx/pdf.html", context, request=request)
        result = BytesIO()
        pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), result, encoding="utf-8")
        if pdf.err:
            return HttpResponse("Gagal membuat PDF.", status=500)
        response = HttpResponse(result.getvalue(), content_type="application/pdf")
        response["Content-Disposition"] = (
            f'inline; filename="Kontrak-{trx.nomor_kontrak}.pdf"'
        )
        return response


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "transaction/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit Transaksi Gadai"
        context["form_subtitle"] = "Perbarui data kontrak gadai"
        context["schemes_data"] = _get_schemes_data()
        return context

    def get_success_url(self):
        return reverse("transaction:detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Transaksi {form.instance.nomor_kontrak} berhasil diperbarui.",
        )
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Periksa kembali data yang Anda masukkan.")
        return super().form_invalid(form)


class TransactionDeleteView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        target = get_object_or_404(Transaction, pk=pk)
        number = target.nomor_kontrak
        try:
            target.delete()
        except ProtectedError:
            return JsonResponse(
                {
                    "success": False,
                    "message": "Transaksi tidak dapat dihapus karena masih digunakan.",
                },
                status=400,
            )
        return JsonResponse(
            {"success": True, "message": f"Transaksi {number} berhasil dihapus."}
        )
