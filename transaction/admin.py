from django.contrib import admin

from transaction.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "nomor_kontrak",
        "customer",
        "collateral",
        "scheme",
        "uang_pinjaman",
        "tanggal_pinjam",
        "tanggal_jatuh_tempo",
        "status_kontrak",
    )
    list_filter = (
        "status_kontrak",
        "scheme",
        "storages",
    )
    search_fields = (
        "nomor_kontrak",
        "customer__name",
        "customer__nik",
        "collateral__name",
        "collateral__code",
    )
    autocomplete_fields = (
        "collateral",
        "storages",
        "customer",
        "scheme",
        "created_by",
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-tanggal_pinjam", "-created_at")
