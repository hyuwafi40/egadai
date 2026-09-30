from django.contrib import messages
from django.urls import reverse

from account.forms import ProfileForm
from account.models import Profile
from account.utils.services import get_profile
from account.views.base import (
    BaseAuthDetailView,
    BaseAuthUpdateView,
)

FORM_TABS = [
    {"id": "identitas", "label": "Identitas", "icon": "fa-id-card"},
    {"id": "pribadi", "label": "Data Pribadi", "icon": "fa-user"},
    {"id": "alamat", "label": "Alamat", "icon": "fa-location-dot"},
    {"id": "kepegawaian", "label": "Kepegawaian", "icon": "fa-briefcase"},
    {"id": "kontak-darurat", "label": "Kontak Darurat", "icon": "fa-phone"},
    {"id": "lainnya", "label": "Lainnya", "icon": "fa-circle-info"},
]


class ProfileDetailView(BaseAuthDetailView):
    model = Profile
    template_name = "account/profile.html"
    context_object_name = "profile_obj"

    def get_object(self, queryset=None):
        return get_profile(self.request.user)


class ProfileUpdateView(BaseAuthUpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "account/profile/form.html"
    context_object_name = "profile_obj"

    def get_object(self, queryset=None):
        return get_profile(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_tabs"] = FORM_TABS
        return context

    def get_success_url(self):
        return reverse("account:profile-detail")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Profil berhasil diperbarui.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Periksa kembali data yang Anda masukkan.")
        return super().form_invalid(form)
