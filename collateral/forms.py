from django import forms
from django.db.models import Q

from config.shared.forms import BaseModelForm
from collateral.models import Collateral
from vault.models import Storages
from vault.utils.constants import StorageStatusChoices


class CollateralForm(BaseModelForm):
    class Meta:
        model = Collateral
        fields = [
            "name",
            "code",
            "status",
            "is_active",
            "category",
            "storages",
            "appraisal_value",
            "intake_date",
            "description",
            "photo",
            "notes",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Contoh: Cincin Emas 24K"}),
            "code": forms.TextInput(attrs={"placeholder": "Contoh: COL-001"}),
            "appraisal_value": forms.NumberInput(
                attrs={"step": "0.01", "placeholder": "Contoh: 5000000"}
            ),
            "intake_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Deskripsi detail barang jaminan...",
                }
            ),
            "photo": forms.FileInput(attrs={"accept": "image/*"}),
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Catatan tambahan...",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = Storages.objects.filter(
            is_active=True,
            status=StorageStatusChoices.TERSEDIA,
        )
        if self.instance and self.instance.pk:
            current_id = getattr(self.instance, "storages_id", None)
            if current_id:
                queryset = Storages.objects.filter(
                    Q(is_active=True, status=StorageStatusChoices.TERSEDIA)
                    | Q(pk=current_id)
                )
        self.fields["storages"].queryset = queryset
