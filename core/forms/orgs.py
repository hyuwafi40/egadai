from django import forms

from core.forms.base import BaseModelForm
from core.models import Orgs


class OrgsForm(BaseModelForm):
    clear_logo = forms.BooleanField(
        required=False,
        label="Hapus logo saat ini",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Orgs
        fields = [
            "name",
            "owner",
            "legal_name",
            "brand_name",
            "company_status",
            "company_type",
            "description",
            "tagline",
            "npwp",
            "license_number",
            "license_date",
            "deed_number",
            "deed_date",
            "last_amendment_number",
            "last_amendment_date",
            "founded_date",
            "founded_place",
            "business_sector",
            "authorized_capital",
            "paid_up_capital",
            "business_scope",
            "address",
            "city",
            "province",
            "postal_code",
            "country",
            "phone",
            "fax",
            "email",
            "website",
            "business_type",
            "products_services",
            "total_branches",
            "total_employees",
            "psp_name",
            "psp_type",
            "vision",
            "mission",
            "latitude",
            "longitude",
            "logo",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Contoh: Pegadaian Cabang Bandung"}
            ),
            "owner": forms.TextInput(
                attrs={"placeholder": "Nama pemilik atau perusahaan induk"}
            ),
            "legal_name": forms.TextInput(
                attrs={"placeholder": "Nama sesuai akta pendirian"}
            ),
            "brand_name": forms.TextInput(
                attrs={"placeholder": "Nama brand yang dikenal publik"}
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Deskripsi singkat tentang perusahaan...",
                }
            ),
            "tagline": forms.TextInput(attrs={"placeholder": "Slogan perusahaan"}),
            "npwp": forms.TextInput(attrs={"placeholder": "00.000.000.0-000.000"}),
            "license_number": forms.TextInput(
                attrs={"placeholder": "Nomor izin usaha dari OJK"}
            ),
            "license_date": forms.DateInput(
                attrs={"placeholder": "Pilih tanggal izin"}
            ),
            "deed_number": forms.TextInput(
                attrs={"placeholder": "Nomor akta pendirian perusahaan"}
            ),
            "deed_date": forms.DateInput(attrs={"placeholder": "Pilih tanggal akta"}),
            "last_amendment_number": forms.TextInput(
                attrs={"placeholder": "Nomor akta perubahan terakhir"}
            ),
            "last_amendment_date": forms.DateInput(
                attrs={"placeholder": "Pilih tanggal perubahan"}
            ),
            "founded_date": forms.DateInput(
                attrs={"placeholder": "Pilih tanggal pendirian"}
            ),
            "founded_place": forms.TextInput(attrs={"placeholder": "Contoh: Bandung"}),
            "business_sector": forms.TextInput(
                attrs={"placeholder": "Contoh: Jasa Keuangan"}
            ),
            "authorized_capital": forms.NumberInput(
                attrs={"step": "0.01", "placeholder": "0.00"}
            ),
            "paid_up_capital": forms.NumberInput(
                attrs={"step": "0.01", "placeholder": "0.00"}
            ),
            "address": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Alamat lengkap kantor pusat..."}
            ),
            "city": forms.TextInput(attrs={"placeholder": "Contoh: Bandung"}),
            "province": forms.TextInput(attrs={"placeholder": "Contoh: Jawa Barat"}),
            "postal_code": forms.TextInput(attrs={"placeholder": "Contoh: 40111"}),
            "country": forms.TextInput(attrs={"placeholder": "Contoh: Indonesia"}),
            "phone": forms.TextInput(attrs={"placeholder": "Contoh: 022-1234567"}),
            "fax": forms.TextInput(attrs={"placeholder": "Contoh: 022-1234568"}),
            "email": forms.EmailInput(
                attrs={"placeholder": "Contoh: info@perusahaan.co.id"}
            ),
            "website": forms.URLInput(attrs={"placeholder": "https://contoh.co.id"}),
            "business_type": forms.TextInput(
                attrs={"placeholder": "Contoh: Gadai Konvensional"}
            ),
            "products_services": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Daftar produk dan layanan yang ditawarkan...",
                }
            ),
            "total_branches": forms.NumberInput(attrs={"placeholder": "Contoh: 100"}),
            "total_employees": forms.NumberInput(attrs={"placeholder": "Contoh: 500"}),
            "psp_name": forms.TextInput(
                attrs={"placeholder": "Nama Pemegang Saham Pengendali"}
            ),
            "vision": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Visi perusahaan..."}
            ),
            "mission": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Misi perusahaan..."}
            ),
            "latitude": forms.NumberInput(
                attrs={"step": "0.000001", "placeholder": "Contoh: -6.2088"}
            ),
            "longitude": forms.NumberInput(
                attrs={"step": "0.000001", "placeholder": "Contoh: 106.8456"}
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
