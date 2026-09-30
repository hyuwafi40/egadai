from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import View

from vault.forms import SchemeForm
from vault.models import Scheme
from vault.utils.constants import SCHEMES_PER_PAGE
from vault.views.base import (
    BaseManagerCreateView,
    BaseManagerUpdateView,
    BaseManagerView,
    ManagerRequiredMixin,
)


class SchemeListView(BaseManagerView):
    template_name = "vault/scheme.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = Scheme.objects.all().order_by("name")
        paginator = Paginator(queryset, SCHEMES_PER_PAGE)
        page_obj = paginator.get_page(self.request.GET.get("page"))
        context["page_obj"] = page_obj
        context["total_schemes"] = queryset.count()
        return context


class SchemeCreateView(BaseManagerCreateView):
    model = Scheme
    form_class = SchemeForm
    template_name = "vault/scheme/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Tambah Scheme"
        context["form_subtitle"] = "Buat skema gadai baru"
        return context

    def get_success_url(self):
        return reverse("vault:scheme-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Scheme {form.instance.name} berhasil dibuat.",
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Periksa kembali data yang Anda masukkan.",
        )
        return super().form_invalid(form)


class SchemeUpdateView(BaseManagerUpdateView):
    model = Scheme
    form_class = SchemeForm
    template_name = "vault/scheme/form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Edit Scheme"
        context["form_subtitle"] = "Perbarui informasi skema gadai"
        return context

    def get_success_url(self):
        return reverse("vault:scheme-list")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(
            self.request,
            f"Scheme {form.instance.name} berhasil diperbarui.",
        )
        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Periksa kembali data yang Anda masukkan.",
        )
        return super().form_invalid(form)


class SchemeDeleteView(LoginRequiredMixin, ManagerRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        target = get_object_or_404(Scheme, pk=pk)
        name = target.name
        target.delete()
        return JsonResponse(
            {"success": True, "message": f"Scheme {name} berhasil dihapus."}
        )
