from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, TemplateView, UpdateView

from core.access import (
    DeveloperRequiredMixin,
    ManagerRequiredMixin,
    RegulerRequiredMixin,
)


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
