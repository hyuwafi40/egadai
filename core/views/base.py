from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

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


class BaseDeveloperView(LoginRequiredMixin, DeveloperRequiredMixin, TemplateView):
    pass


class BaseRegulerView(LoginRequiredMixin, RegulerRequiredMixin, TemplateView):
    pass
