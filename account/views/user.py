from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from account.forms import UserCreateForm, UserUpdateForm
from account.utils.constants import (
    DEFAULT_PASSWORD,
    USERS_PER_PAGE,
    VISIBLE_JOB_CHOICES,
    JobChoices,
)
from account.views.base import BaseManagerView, ManagerRequiredMixin

User = get_user_model()


class UserListView(BaseManagerView):
    template_name = "account/user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = User.objects.exclude(job=JobChoices.DEVELOPER).order_by(
            "-created_at"
        )
        paginator = Paginator(queryset, USERS_PER_PAGE)
        page_obj = paginator.get_page(self.request.GET.get("page"))
        context["page_obj"] = page_obj
        context["total_users"] = queryset.count()
        context["job_choices"] = VISIBLE_JOB_CHOICES
        context["default_password"] = DEFAULT_PASSWORD
        return context


class UserCreateView(LoginRequiredMixin, ManagerRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        if not form.is_valid():
            return JsonResponse(
                {"success": False, "errors": form.errors.get_json_data()},
                status=400,
            )
        target_job = form.cleaned_data["job"]
        if target_job == JobChoices.DEVELOPER:
            raise PermissionDenied
        user = form.save()
        return JsonResponse(
            {
                "success": True,
                "message": f"User {user.username} berhasil dibuat dengan password default.",
            }
        )


class UserUpdateView(LoginRequiredMixin, ManagerRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        target = get_object_or_404(User, pk=pk)
        if target.job == JobChoices.DEVELOPER:
            raise PermissionDenied
        form = UserUpdateForm(request.POST, instance=target)
        if not form.is_valid():
            return JsonResponse(
                {"success": False, "errors": form.errors.get_json_data()},
                status=400,
            )
        new_job = form.cleaned_data["job"]
        if new_job == JobChoices.DEVELOPER:
            raise PermissionDenied
        user = form.save()
        return JsonResponse(
            {"success": True, "message": f"User {user.username} berhasil diperbarui."}
        )


class UserDeleteView(LoginRequiredMixin, ManagerRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        target = get_object_or_404(User, pk=pk)
        if target.job == JobChoices.DEVELOPER:
            raise PermissionDenied
        if target.pk == request.user.pk:
            raise PermissionDenied
        username = target.username
        target.delete()
        return JsonResponse(
            {"success": True, "message": f"User {username} berhasil dihapus."}
        )


class UserPasswordResetView(LoginRequiredMixin, ManagerRequiredMixin, View):
    http_method_names = ["post"]

    def post(self, request, pk, *args, **kwargs):
        target = get_object_or_404(User, pk=pk)
        if target.job == JobChoices.DEVELOPER:
            raise PermissionDenied
        target.set_password(DEFAULT_PASSWORD)
        target.save()
        return JsonResponse(
            {
                "success": True,
                "message": f"Password {target.username} berhasil direset.",
            }
        )
