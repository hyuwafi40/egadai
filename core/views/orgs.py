from core.forms import OrgsForm
from core.models import Orgs
from core.views.base import (
    BaseManagerDetailView,
    BaseManagerUpdateView,
    SingletonObjectMixin,
    SingletonSuccessMixin,
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


class OrgsDetailView(SingletonObjectMixin, BaseManagerDetailView):
    model = Orgs
    template_name = "core/orgs.html"
    context_object_name = "orgs_obj"


class OrgsUpdateView(
    SingletonObjectMixin,
    SingletonSuccessMixin,
    BaseManagerUpdateView,
):
    model = Orgs
    form_class = OrgsForm
    template_name = "core/orgs/form.html"
    success_url_name = "core:orgs-detail"
    success_message = "Organisasi berhasil diperbarui."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_tabs"] = FORM_TABS
        return context
