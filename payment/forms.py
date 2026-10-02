from django import forms

from config.shared.forms import BaseModelForm, DateInput
from payment.models import Payment


class PaymentForm(BaseModelForm):
    class Meta:
        model = Payment
        fields = [
            "nomor_pembayaran",
            "tanggal_bayar",
            "jumlah_bayar",
            "tipe_pembayaran",
            "metode_pembayaran",
            "catatan",
        ]
        labels = {
            "nomor_pembayaran": "Nomor Pembayaran",
            "tanggal_bayar": "Tanggal Bayar",
            "jumlah_bayar": "Jumlah Bayar",
            "tipe_pembayaran": "Tipe Pembayaran",
            "metode_pembayaran": "Metode Pembayaran",
            "catatan": "Catatan",
        }
        widgets = {
            "nomor_pembayaran": forms.TextInput(
                attrs={
                    "placeholder": "Kosongkan agar dibuat otomatis",
                    "autocomplete": "off",
                }
            ),
            "tanggal_bayar": DateInput(),
            "jumlah_bayar": forms.TextInput(
                attrs={
                    "inputmode": "numeric",
                    "autocomplete": "off",
                    "placeholder": "Contoh: 50000",
                    "data-currency": "true",
                }
            ),
            "catatan": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Catatan tambahan (opsional)",
                }
            ),
        }
