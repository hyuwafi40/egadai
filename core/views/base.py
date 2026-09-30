from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.views.generic import DetailView, TemplateView, UpdateView

from core.access import (
    DeveloperRequiredMixin,
    ManagerRequiredMixin,
    RegulerRequiredMixin,
)


class SingletonObjectMixin:
    def get_object(self, queryset=None):
        manager = self.model.objects
        if hasattr(manager, "get_current"):
            obj = manager.get_current()
            if obj is not None:
                return obj
        obj, _ = manager.get_or_create(pk=1)
        return obj


class SingletonSuccessMixin:
    success_url_name = None
    success_message = "Data berhasil diperbarui."
    error_message = "Periksa kembali data yang Anda masukkan."

    def get_success_url(self):
        if not self.success_url_name:
            raise ImproperlyConfigured("success_url_name wajib diisi pada view ini.")
        return reverse(self.success_url_name)

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def form_invalid(self, form):
        messages.error(self.request, self.error_message)
        return super().form_invalid(form)


class BaseView(TemplateView):
    pass


class BaseAuthView(LoginRequiredMixin, TemplateView):
    pass


class BaseManagerView(LoginRequiredMixin, ManagerRequiredMixin, TemplateView):
    pass


class BaseManagerDetailView(LoginRequiredMixin, ManagerRequiredMixin, DetailView):
    pass


class BaseManagerUpdateView(LoginRequiredMixin, ManagerRequiredMixin, UpdateView):
    pass


class BaseDeveloperView(LoginRequiredMixin, DeveloperRequiredMixin, TemplateView):
    pass


class BaseDeveloperDetailView(LoginRequiredMixin, DeveloperRequiredMixin, DetailView):
    pass


class BaseDeveloperUpdateView(LoginRequiredMixin, DeveloperRequiredMixin, UpdateView):
    pass


class BaseRegulerView(LoginRequiredMixin, RegulerRequiredMixin, TemplateView):
    pass
