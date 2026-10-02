from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, TemplateView, UpdateView

from collateral.forms import CollateralForm
from collateral.models import Collateral
from collateral.utils.constants import COLLATERALS_PER_PAGE


class CollateralListView(LoginRequiredMixin, TemplateView):
    template_name = "collateral/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Collateral.objects.select_related("category", "storages").order_by(
            "name"
        )
        paginator = Paginator(queryset, COLLATERALS_PER_PAGE)
        page_obj = paginator.get_page(self.request.GET.get("page"))
        context["page_obj"] = page_obj
        context["total_collaterals"] = queryset.count()
        return context


class CollateralCreateView(LoginRequiredMixin, CreateView):
    model = Collateral
    form_class = CollateralForm
    template_name = "collateral/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Tambah Barang Jaminan"
        context["form_subtitle"] = "Buat data barang jaminan baru"
        return context

    def get_success_url(self):
        return reverse("collateral:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Barang jaminan {form.instance.name} berhasil dibuat.",
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Periksa kembali data yang Anda masukkan.",
        )
        return super().form_invalid(form)


class CollateralUpdateView(LoginRequiredMixin, UpdateView):
    model = Collateral
    form_class = CollateralForm
    template_name = "collateral/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit Barang Jaminan"
        context["form_subtitle"] = "Perbarui data barang jaminan"
        return context

    def get_success_url(self):
        return reverse("collateral:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Barang jaminan {form.instance.name} berhasil diperbarui.",
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Periksa kembali data yang Anda masukkan.",
        )
        return super().form_invalid(form)


class CollateralDeleteView(LoginRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        target = get_object_or_404(Collateral, pk=pk)
        name = target.name
        try:
            target.delete()
        except ProtectedError:
            return JsonResponse(
                {
                    "success": False,
                    "message": (
                        "Barang jaminan tidak dapat dihapus karena masih " "digunakan."
                    ),
                },
                status=400,
            )
        return JsonResponse(
            {"success": True, "message": f"Barang jaminan {name} berhasil dihapus."}
        )
