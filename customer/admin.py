from django.contrib import admin

from customer.models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "nik",
        "customer_code",
        "phone",
        "city",
        "is_active",
        "updated_at",
    )
    list_filter = ("is_active", "gender", "marital_status", "province")
    search_fields = ("name", "nik", "customer_code", "phone", "email")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("name",)
