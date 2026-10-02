from django import forms

from config.shared.forms import BaseModelForm
from vault.models import Storages


class StoragesForm(BaseModelForm):
    class Meta:
        model = Storages
        fields = [
            "name",
            "kode_gudang",
            "status",
            "is_active",
            "address",
            "city",
            "province",
            "postal_code",
            "phone",
            "penanggung_jawab",
            "capacity",
            "current_occupancy",
            "latitude",
            "longitude",
            "description",
            "notes",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Contoh: Gudang Pusat"}),
            "kode_gudang": forms.TextInput(attrs={"placeholder": "Contoh: GDG-001"}),
            "address": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Alamat lengkap gudang...",
                }
            ),
            "city": forms.TextInput(attrs={"placeholder": "Contoh: Bandung"}),
            "province": forms.TextInput(attrs={"placeholder": "Contoh: Jawa Barat"}),
            "postal_code": forms.TextInput(attrs={"placeholder": "Contoh: 40111"}),
            "phone": forms.TextInput(attrs={"placeholder": "Contoh: 022-1234567"}),
            "penanggung_jawab": forms.TextInput(
                attrs={"placeholder": "Nama petugas gudang"}
            ),
            "capacity": forms.NumberInput(
                attrs={"min": 0, "placeholder": "Contoh: 1000"}
            ),
            "current_occupancy": forms.NumberInput(
                attrs={
                    "readonly": True,
                    "min": 0,
                }
            ),
            "latitude": forms.NumberInput(
                attrs={"step": "0.000001", "placeholder": "Contoh: -6.2088"}
            ),
            "longitude": forms.NumberInput(
                attrs={"step": "0.000001", "placeholder": "Contoh: 106.8456"}
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Deskripsi singkat gudang...",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Catatan operasional...",
                }
            ),
        }
