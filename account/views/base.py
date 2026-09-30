from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView, TemplateView, UpdateView

from account.utils.constants import JobChoices

MANAGER_ROLES = (JobChoices.DEVELOPER, JobChoices.ADMINISTRATOR)


class ManagerRequiredMixin:
    allowed_jobs = MANAGER_ROLES

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not getattr(user, "is_authenticated", False):
            raise PermissionDenied
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        if getattr(user, "job", None) not in self.allowed_jobs:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class BaseView(TemplateView):
    pass


class BaseAuthView(LoginRequiredMixin, TemplateView):
    pass


class BaseAuthDetailView(LoginRequiredMixin, DetailView):
    pass


class BaseAuthUpdateView(LoginRequiredMixin, UpdateView):
    pass


class BaseManagerView(LoginRequiredMixin, ManagerRequiredMixin, TemplateView):
    pass
