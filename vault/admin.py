from django.contrib import admin

from vault.models import Category, Scheme, Storages


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "updated_at")
    search_fields = ("name", "code", "description")
    ordering = ("name",)


@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "bunga",
        "periode_bunga",
        "durasi_maksimal_hari",
        "denda_persen_perhari",
        "biaya_admin",
    )
    list_filter = ("periode_bunga",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Storages)
class StoragesAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "kode_gudang",
        "status",
        "city",
        "province",
        "capacity",
        "current_occupancy",
        "is_active",
    )
    list_filter = ("status", "is_active", "province")
    search_fields = ("name", "kode_gudang", "address", "city", "province")
    ordering = ("name",)
