from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView

from vault.utils.constants import MANAGER_ROLES


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


class BaseManagerView(LoginRequiredMixin, ManagerRequiredMixin, TemplateView):
    pass
