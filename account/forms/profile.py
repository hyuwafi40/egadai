from django import forms

from account.forms.base import BasePhotoModelForm
from account.models import Profile


class ProfileForm(BasePhotoModelForm):
    class Meta:
        model = Profile
        fields = [
            "employee_id",
            "full_name",
            "nickname",
            "photo",
            "gender",
            "date_of_birth",
            "place_of_birth",
            "marital_status",
            "religion",
            "phone",
            "address",
            "city",
            "province",
            "postal_code",
            "country",
            "department",
            "position",
            "employment_type",
            "hire_date",
            "emergency_contact_name",
            "emergency_contact_phone",
            "about",
        ]
        widgets = {
            "employee_id": forms.TextInput(attrs={"placeholder": "Contoh: EMP-0001"}),
            "full_name": forms.TextInput(
                attrs={"placeholder": "Nama lengkap sesuai identitas"}
            ),
            "nickname": forms.TextInput(
                attrs={"placeholder": "Nama panggilan sehari-hari"}
            ),
            "photo": forms.FileInput(attrs={"accept": "image/*"}),
            "date_of_birth": forms.DateInput(
                attrs={"placeholder": "Pilih tanggal lahir"}
            ),
            "place_of_birth": forms.TextInput(attrs={"placeholder": "Contoh: Bandung"}),
            "religion": forms.TextInput(attrs={"placeholder": "Contoh: Islam"}),
            "phone": forms.TextInput(attrs={"placeholder": "Contoh: 0812-3456-7890"}),
            "address": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Alamat lengkap tempat tinggal..."}
            ),
            "city": forms.TextInput(attrs={"placeholder": "Contoh: Bandung"}),
            "province": forms.TextInput(attrs={"placeholder": "Contoh: Jawa Barat"}),
            "postal_code": forms.TextInput(attrs={"placeholder": "Contoh: 40111"}),
            "country": forms.TextInput(attrs={"placeholder": "Contoh: Indonesia"}),
            "department": forms.TextInput(attrs={"placeholder": "Contoh: Operasional"}),
            "position": forms.TextInput(attrs={"placeholder": "Contoh: Kasir"}),
            "hire_date": forms.DateInput(
                attrs={"placeholder": "Pilih tanggal masuk kerja"}
            ),
            "emergency_contact_name": forms.TextInput(
                attrs={"placeholder": "Nama kontak darurat"}
            ),
            "emergency_contact_phone": forms.TextInput(
                attrs={"placeholder": "Contoh: 0812-3456-7890"}
            ),
            "about": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Deskripsi singkat tentang Anda..."}
            ),
        }
