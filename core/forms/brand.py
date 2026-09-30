from django import forms

from core.forms.base import BaseModelForm
from core.models import Brand


class BrandForm(BaseModelForm):
    clear_logo = forms.BooleanField(
        required=False,
        label="Hapus logo saat ini",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

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

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.cleaned_data.get("clear_logo") and not self.cleaned_data.get("logo"):
            instance.logo = None
        if commit:
            instance.save()
            self._save_m2m()
        return instance
