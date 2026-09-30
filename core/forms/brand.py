from django import forms

from core.forms.base import BaseLogoModelForm
from core.models import Brand


class BrandForm(BaseLogoModelForm):
    class Meta:
        model = Brand
        fields = [
            "name",
            "description",
            "version",
            "creator",
            "facebook",
            "instagram",
            "tiktok",
            "youtube",
            "logo",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Contoh: Aplikasi Pegadaian"}
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Deskripsi singkat tentang aplikasi...",
                }
            ),
            "version": forms.TextInput(attrs={"placeholder": "Contoh: 1.0.0"}),
            "creator": forms.TextInput(attrs={"placeholder": "Nama pembuat atau tim"}),
            "facebook": forms.URLInput(
                attrs={"placeholder": "https://facebook.com/username"}
            ),
            "instagram": forms.URLInput(
                attrs={"placeholder": "https://instagram.com/username"}
            ),
            "tiktok": forms.URLInput(
                attrs={"placeholder": "https://www.tiktok.com/@username"}
            ),
            "youtube": forms.URLInput(
                attrs={"placeholder": "https://youtube.com/@username"}
            ),
            "logo": forms.FileInput(attrs={"accept": "image/*"}),
        }
