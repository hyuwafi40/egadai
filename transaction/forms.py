from django import forms
from django.db.models import Q

from config.shared.forms import BaseModelForm
from collateral.models import Collateral
from customer.models import Customer
from transaction.models import Transaction
from vault.models import Scheme, Storages


class TransactionForm(BaseModelForm):
    class Meta:
        model = Transaction
        fields = [
            "nomor_kontrak",
            "status_kontrak",
            "customer",
            "collateral",
            "scheme",
            "storages",
            "tanggal_pinjam",
            "tanggal_jatuh_tempo",
            "uang_pinjaman",
            "tujuan_pinjaman",
        ]
        widgets = {
            "nomor_kontrak": forms.TextInput(
                attrs={
                    "placeholder": "Kosongkan untuk auto-generate",
                    "autocomplete": "off",
                }
            ),
            "tanggal_pinjam": forms.DateInput(attrs={"type": "date"}),
            "tanggal_jatuh_tempo": forms.DateInput(attrs={"type": "date"}),
            "uang_pinjaman": forms.TextInput(
                attrs={
                    "inputmode": "numeric",
                    "autocomplete": "off",
                    "placeholder": "Contoh: 1000000",
                    "data-currency": "true",
                }
            ),
            "tujuan_pinjaman": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Contoh: Modal usaha dagang",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["customer"].queryset = self._active_with_current(
            Customer, "customer"
        )
        self.fields["collateral"].queryset = self._active_with_current(
            Collateral, "collateral"
        )
        self.fields["storages"].queryset = self._active_with_current(
            Storages, "storages"
        )
        self.fields["scheme"].queryset = Scheme.objects.all()

    def _active_with_current(self, model, field_name):
        queryset = model.objects.filter(is_active=True)
        if self.instance and self.instance.pk:
            current_id = getattr(self.instance, f"{field_name}_id", None)
            if current_id:
                queryset = model.objects.filter(Q(is_active=True) | Q(pk=current_id))
        return queryset
