from django.contrib import admin

from collateral.models import Collateral


@admin.register(Collateral)
class CollateralAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "owner",
        "category",
        "storages",
        "status",
        "appraisal_value",
        "is_active",
    )
    list_filter = (
        "status",
        "category",
        "storages",
        "is_active",
    )
    search_fields = (
        "name",
        "code",
        "owner__name",
        "owner__nik",
    )
    autocomplete_fields = (
        "owner",
        "category",
        "storages",
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)
