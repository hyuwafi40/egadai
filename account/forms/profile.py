from django import forms

from account.forms.base import BasePhotoModelForm
from account.models import Profile
from config.shared.forms import DateInput


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
        labels = {
            "employee_id": "ID Pegawai",
            "full_name": "Nama Lengkap",
            "nickname": "Nama Panggilan",
            "photo": "Foto Profil",
            "gender": "Jenis Kelamin",
            "date_of_birth": "Tanggal Lahir",
            "place_of_birth": "Tempat Lahir",
            "marital_status": "Status Pernikahan",
            "religion": "Agama",
            "phone": "Nomor HP",
            "address": "Alamat",
            "city": "Kota",
            "province": "Provinsi",
            "postal_code": "Kode Pos",
            "country": "Negara",
            "department": "Departemen",
            "position": "Jabatan",
            "employment_type": "Status Kerja",
            "hire_date": "Tanggal Masuk",
            "emergency_contact_name": "Nama Kontak Darurat",
            "emergency_contact_phone": "HP Kontak Darurat",
            "about": "Tentang",
        }
        widgets = {
            "employee_id": forms.TextInput(attrs={"placeholder": "Contoh: EMP-0001"}),
            "full_name": forms.TextInput(
                attrs={"placeholder": "Nama lengkap sesuai identitas"}
            ),
            "nickname": forms.TextInput(
                attrs={"placeholder": "Nama panggilan sehari-hari"}
            ),
            "date_of_birth": DateInput(),
            "place_of_birth": forms.TextInput(attrs={"placeholder": "Contoh: Bandung"}),
            "religion": forms.TextInput(attrs={"placeholder": "Contoh: Islam"}),
            "phone": forms.TextInput(attrs={"placeholder": "Contoh: 081234567890"}),
            "address": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Tulis alamat lengkap"}
            ),
            "city": forms.TextInput(attrs={"placeholder": "Contoh: Bandung"}),
            "province": forms.TextInput(attrs={"placeholder": "Contoh: Jawa Barat"}),
            "postal_code": forms.TextInput(attrs={"placeholder": "Contoh: 40111"}),
            "country": forms.TextInput(attrs={"placeholder": "Contoh: Indonesia"}),
            "department": forms.TextInput(attrs={"placeholder": "Contoh: Operasional"}),
            "position": forms.TextInput(attrs={"placeholder": "Contoh: Kasir"}),
            "hire_date": DateInput(),
            "emergency_contact_name": forms.TextInput(
                attrs={"placeholder": "Nama orang yang bisa dihubungi"}
            ),
            "emergency_contact_phone": forms.TextInput(
                attrs={"placeholder": "Contoh: 081234567890"}
            ),
            "about": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Ceritakan singkat tentang Anda"}
            ),
        }
