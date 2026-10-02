from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View

from vault.forms import StoragesForm
from vault.models import Storages
from vault.utils.constants import STORAGES_PER_PAGE
from vault.views.base import (
    BaseManagerCreateView,
    BaseManagerUpdateView,
    BaseManagerView,
    ManagerRequiredMixin,
)


class StoragesListView(BaseManagerView):
    template_name = "vault/storages.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Storages.objects.all().order_by("name")
        paginator = Paginator(queryset, STORAGES_PER_PAGE)
        page_obj = paginator.get_page(self.request.GET.get("page"))
        context["page_obj"] = page_obj
        context["total_storages"] = queryset.count()
        return context


class StoragesCreateView(BaseManagerCreateView):
    model = Storages
    form_class = StoragesForm
    template_name = "vault/storages/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Tambah Gudang"
        context["form_subtitle"] = "Buat data gudang baru"
        return context

    def get_success_url(self):
        return reverse("vault:storages-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Gudang {form.instance.name} berhasil dibuat.",
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Periksa kembali data yang Anda masukkan.",
        )
        return super().form_invalid(form)


class StoragesUpdateView(BaseManagerUpdateView):
    model = Storages
    form_class = StoragesForm
    template_name = "vault/storages/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit Gudang"
        context["form_subtitle"] = "Perbarui informasi gudang"
        return context

    def get_success_url(self):
        return reverse("vault:storages-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Gudang {form.instance.name} berhasil diperbarui.",
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Periksa kembali data yang Anda masukkan.",
        )
        return super().form_invalid(form)


class StoragesDeleteView(LoginRequiredMixin, ManagerRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        target = get_object_or_404(Storages, pk=pk)
        name = target.name
        target.delete()
        return JsonResponse(
            {"success": True, "message": f"Gudang {name} berhasil dihapus."}
        )
