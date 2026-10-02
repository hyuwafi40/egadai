from django import forms

from config.shared.forms import BaseModelForm
from customer.models import Customer


class CustomerForm(BaseModelForm):
    class Meta:
        model = Customer
        fields = [
            "name",
            "nik",
            "customer_code",
            "gender",
            "date_of_birth",
            "occupation",
            "marital_status",
            "phone",
            "email",
            "address",
            "city",
            "province",
            "emergency_contact_name",
            "emergency_contact_phone",
            "emergency_contact_relationship",
            "photo",
            "selfie",
            "notes",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Nama lengkap nasabah"}),
            "nik": forms.TextInput(
                attrs={
                    "placeholder": "16 digit NIK",
                    "inputmode": "numeric",
                    "maxlength": "16",
                }
            ),
            "customer_code": forms.TextInput(attrs={"placeholder": "Contoh: CUST-001"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "occupation": forms.TextInput(
                attrs={"placeholder": "Contoh: Pegawai Swasta"}
            ),
            "phone": forms.TextInput(attrs={"placeholder": "Contoh: 0812-3456-7890"}),
            "email": forms.EmailInput(
                attrs={"placeholder": "Contoh: nasabah@email.com"}
            ),
            "address": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Alamat lengkap..."}
            ),
            "city": forms.TextInput(attrs={"placeholder": "Contoh: Bandung"}),
            "province": forms.TextInput(attrs={"placeholder": "Contoh: Jawa Barat"}),
            "emergency_contact_name": forms.TextInput(
                attrs={"placeholder": "Nama kontak darurat"}
            ),
            "emergency_contact_phone": forms.TextInput(
                attrs={"placeholder": "Contoh: 0812-3456-7890"}
            ),
            "emergency_contact_relationship": forms.TextInput(
                attrs={"placeholder": "Contoh: Istri, Ayah, Saudara"}
            ),
            "photo": forms.FileInput(attrs={"accept": "image/*"}),
            "selfie": forms.FileInput(attrs={"accept": "image/*"}),
            "notes": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Catatan tambahan..."}
            ),
        }
