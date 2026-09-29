from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from account.models import Profile, User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0
    verbose_name = "Profile"
    verbose_name_plural = "Profile"


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]
    list_display = (
        "username",
        "email",
        "job",
        "is_active",
        "is_staff",
    )
    list_filter = (
        "job",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    search_fields = (
        "username",
        "email",
        "profile__full_name",
    )
    ordering = ("-created_at",)

    fieldsets = BaseUserAdmin.fieldsets + (("Job", {"fields": ("job",)}),)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "employee_id",
        "full_name",
        "department",
        "position",
    )
    search_fields = (
        "user__username",
        "user__email",
        "employee_id",
        "full_name",
    )
    list_filter = (
        "department",
        "employment_type",
        "gender",
    )
    autocomplete_fields = ("user",)
