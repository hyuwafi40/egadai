from django import forms

from config.shared.forms import BaseModelForm
from vault.models import Category


class CategoryForm(BaseModelForm):
    class Meta:
        model = Category
        fields = [
            "name",
            "code",
            "description",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Contoh: Emas"}),
            "code": forms.TextInput(attrs={"placeholder": "Contoh: EMAS"}),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Deskripsi singkat kategori...",
                }
            ),
        }
