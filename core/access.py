from django.core.exceptions import PermissionDenied

from account.utils.constants import JobChoices
from config.shared.access import MANAGER_ROLES

ALL_ROLES = (
    JobChoices.DEVELOPER,
    JobChoices.ADMINISTRATOR,
    JobChoices.REGULER,
)

DEVELOPER_ROLES = (JobChoices.DEVELOPER,)

REGULER_ROLES = (JobChoices.REGULER,)


class JobRequiredMixin:
    allowed_jobs = ()

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not getattr(user, "is_authenticated", False):
            raise PermissionDenied
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        job = getattr(user, "job", None)
        if job not in self.allowed_jobs:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class ManagerRequiredMixin(JobRequiredMixin):
    allowed_jobs = MANAGER_ROLES


class DeveloperRequiredMixin(JobRequiredMixin):
    allowed_jobs = DEVELOPER_ROLES


class RegulerRequiredMixin(JobRequiredMixin):
    allowed_jobs = REGULER_ROLES
