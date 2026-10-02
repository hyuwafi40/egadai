from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView

from transaction.forms import TransactionForm
from transaction.models import Transaction
from transaction.utils.constants import TRANSACTIONS_PER_PAGE
from vault.models import Scheme


def _get_schemes_data():
    data = {}
    for scheme in Scheme.objects.all():
        data[str(scheme.pk)] = scheme.durasi_maksimal_hari
    return data


class TransactionListView(LoginRequiredMixin, TemplateView):
    template_name = "transaction/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Transaction.objects.select_related(
            "customer",
            "collateral",
            "scheme",
            "storages",
            "created_by",
        ).order_by("-tanggal_pinjam", "-created_at")
        paginator = Paginator(queryset, TRANSACTIONS_PER_PAGE)
        page_obj = paginator.get_page(self.request.GET.get("page"))
        context["page_obj"] = page_obj
        context["total_transactions"] = queryset.count()
        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    model = Transaction
    form_class = TransactionForm
    template_name = "transaction/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Tambah Transaksi Gadai"
        context["form_subtitle"] = "Buat kontrak gadai baru"
        context["schemes_data"] = _get_schemes_data()
        return context

    def get_success_url(self):
        return reverse("transaction:list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Transaksi {form.instance.nomor_kontrak} berhasil dibuat.",
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Periksa kembali data yang Anda masukkan.",
        )
        return super().form_invalid(form)


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
        return reverse("transaction:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Transaksi {form.instance.nomor_kontrak} berhasil diperbarui.",
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Periksa kembali data yang Anda masukkan.",
        )
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
                    "message": (
                        "Transaksi tidak dapat dihapus karena masih " "digunakan."
                    ),
                },
                status=400,
            )
        return JsonResponse(
            {"success": True, "message": f"Transaksi {number} berhasil dihapus."}
        )
