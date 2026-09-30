from django.contrib import messages
from django.urls import reverse

from core.forms import OrgsForm
from core.models import Orgs
from core.views.base import (
    BaseManagerDetailView,
    BaseManagerUpdateView,
)

FORM_TABS = [
    {"id": "identitas", "label": "Identitas", "icon": "fa-id-card"},
    {"id": "legalitas", "label": "Legalitas", "icon": "fa-file-contract"},
    {"id": "permodalan", "label": "Permodalan", "icon": "fa-coins"},
    {"id": "alamat", "label": "Alamat & Kontak", "icon": "fa-location-dot"},
    {"id": "bisnis", "label": "Bisnis", "icon": "fa-briefcase"},
    {"id": "visi-misi", "label": "Visi & Misi", "icon": "fa-bullseye"},
    {"id": "geografis", "label": "Geografis", "icon": "fa-map-pin"},
    {"id": "logo", "label": "Logo", "icon": "fa-image"},
]


class OrgsDetailView(BaseManagerDetailView):
    model = Orgs
    template_name = "core/orgs.html"
    context_object_name = "orgs_obj"

    def get_object(self, queryset=None):
        orgs, _ = Orgs.objects.get_or_create(pk=1)
        return orgs


class OrgsUpdateView(BaseManagerUpdateView):
    model = Orgs
    form_class = OrgsForm
    template_name = "core/orgs/form.html"

    def get_object(self, queryset=None):
        orgs, _ = Orgs.objects.get_or_create(pk=1)
        return orgs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_tabs"] = FORM_TABS
        return context

    def get_success_url(self):
        return reverse("core:orgs-detail")

    def form_valid(self, form):
        messages.success(self.request, "Organisasi berhasil diperbarui.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Periksa kembali data yang Anda masukkan.")
        return super().form_invalid(form)
