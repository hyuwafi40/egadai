from django import forms

from config.shared.forms import BaseModelForm
from vault.models import Scheme


class SchemeForm(BaseModelForm):
    class Meta:
        model = Scheme
        fields = [
            "name",
            "bunga",
            "periode_bunga",
            "durasi_maksimal_hari",
            "denda_persen_perhari",
            "biaya_admin",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Contoh: Reguler 7 Hari"}),
            "bunga": forms.NumberInput(
                attrs={"step": "0.01", "placeholder": "Contoh: 1.5"}
            ),
            "durasi_maksimal_hari": forms.NumberInput(
                attrs={"min": 1, "placeholder": "Contoh: 7"}
            ),
            "denda_persen_perhari": forms.NumberInput(
                attrs={"step": "0.1", "placeholder": "0.5"}
            ),
            "biaya_admin": forms.TextInput(
                attrs={
                    "inputmode": "numeric",
                    "autocomplete": "off",
                    "placeholder": "Contoh: 5000",
                    "data-currency": "true",
                }
            ),
        }
