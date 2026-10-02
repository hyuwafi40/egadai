from django.contrib import admin

from payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "nomor_pembayaran",
        "transaction",
        "tanggal_bayar",
        "jumlah_bayar",
        "tipe_pembayaran",
        "metode_pembayaran",
    )
    list_filter = (
        "tipe_pembayaran",
        "metode_pembayaran",
        "tanggal_bayar",
    )
    search_fields = (
        "nomor_pembayaran",
        "transaction__nomor_kontrak",
        "transaction__customer__name",
        "transaction__customer__nik",
    )
    autocomplete_fields = (
        "transaction",
        "created_by",
    )
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-tanggal_bayar", "-created_at")
