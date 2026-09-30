from django.contrib import messages
from django.urls import reverse

from core.forms import BrandForm
from core.models import Brand
from core.views.base import (
    BaseDeveloperDetailView,
    BaseDeveloperUpdateView,
)


class BrandDetailView(BaseDeveloperDetailView):
    model = Brand
    template_name = "core/brand.html"
    context_object_name = "brand_obj"

    def get_object(self, queryset=None):
        brand, _ = Brand.objects.get_or_create(pk=1)
        return brand


class BrandUpdateView(BaseDeveloperUpdateView):
    model = Brand
    form_class = BrandForm
    template_name = "core/brand/form.html"

    def get_object(self, queryset=None):
        brand, _ = Brand.objects.get_or_create(pk=1)
        return brand

    def get_success_url(self):
        return reverse("core:brand-detail")

    def form_valid(self, form):
        messages.success(self.request, "Brand berhasil diperbarui.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Periksa kembali data yang Anda masukkan.")
        return super().form_invalid(form)
