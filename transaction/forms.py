from django import forms
from django.db.models import Q

from config.shared.forms import BaseModelForm, DateInput
from collateral.models import Collateral
from customer.models import Customer
from transaction.models import Transaction
from vault.models import Scheme, Storages
from vault.utils.constants import StorageStatusChoices


def _active_storages(current_id=None):
    qs = Storages.objects.filter(
        is_active=True,
        status=StorageStatusChoices.TERSEDIA,
    )
    if current_id:
        qs = Storages.objects.filter(
            Q(is_active=True, status=StorageStatusChoices.TERSEDIA) | Q(pk=current_id)
        )
    return qs


class TransactionForm(BaseModelForm):
    class Meta:
        model = Transaction
        fields = [
            "nomor_kontrak",
            "status_kontrak",
            "customer",
            "collateral",
            "scheme",
            "storages",
            "tanggal_pinjam",
            "tanggal_jatuh_tempo",
            "uang_pinjaman",
            "tujuan_pinjaman",
        ]
        widgets = {
            "nomor_kontrak": forms.TextInput(
                attrs={
                    "placeholder": "Kosongkan agar dibuat otomatis",
                    "autocomplete": "off",
                }
            ),
            "tanggal_pinjam": DateInput(),
            "tanggal_jatuh_tempo": DateInput(),
            "uang_pinjaman": forms.TextInput(
                attrs={
                    "inputmode": "numeric",
                    "autocomplete": "off",
                    "placeholder": "Contoh: 1000000",
                    "data-currency": "true",
                }
            ),
            "tujuan_pinjaman": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Contoh: Modal usaha dagang"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["customer"].queryset = self._active_with_current(
            Customer, "customer"
        )
        self.fields["collateral"].queryset = self._active_with_current(
            Collateral, "collateral"
        )
        self.fields["scheme"].queryset = Scheme.objects.all()
        current_storages = None
        if self.instance and self.instance.pk:
            current_storages = getattr(self.instance, "storages_id", None)
        self.fields["storages"].queryset = _active_storages(current_storages)

    def _active_with_current(self, model, field_name):
        queryset = model.objects.filter(is_active=True)
        if self.instance and self.instance.pk:
            current_id = getattr(self.instance, f"{field_name}_id", None)
            if current_id:
                queryset = model.objects.filter(Q(is_active=True) | Q(pk=current_id))
        return queryset


class CustomerQuickForm(BaseModelForm):
    class Meta:
        model = Customer
        fields = [
            "name",
            "nik",
            "customer_code",
            "photo",
            "selfie",
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
            "notes",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Contoh: Budi Santoso"}),
            "nik": forms.TextInput(
                attrs={
                    "placeholder": "16 angka sesuai KTP",
                    "inputmode": "numeric",
                    "maxlength": "16",
                }
            ),
            "customer_code": forms.TextInput(
                attrs={"placeholder": "Kosongkan agar dibuat otomatis"}
            ),
            "date_of_birth": DateInput(),
            "occupation": forms.TextInput(attrs={"placeholder": "Contoh: Pedagang"}),
            "phone": forms.TextInput(attrs={"placeholder": "Contoh: 081234567890"}),
            "email": forms.EmailInput(attrs={"placeholder": "Contoh: budi@email.com"}),
            "address": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Tulis alamat lengkap"}
            ),
            "city": forms.TextInput(attrs={"placeholder": "Contoh: Bandung"}),
            "province": forms.TextInput(attrs={"placeholder": "Contoh: Jawa Barat"}),
            "emergency_contact_name": forms.TextInput(
                attrs={"placeholder": "Nama orang yang bisa dihubungi"}
            ),
            "emergency_contact_phone": forms.TextInput(
                attrs={"placeholder": "Contoh: 081234567890"}
            ),
            "emergency_contact_relationship": forms.TextInput(
                attrs={"placeholder": "Contoh: Istri, Suami, Ayah"}
            ),
            "photo": forms.FileInput(attrs={"accept": "image/*"}),
            "selfie": forms.FileInput(attrs={"accept": "image/*"}),
            "notes": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Catatan tambahan (opsional)"}
            ),
        }


class CollateralQuickForm(BaseModelForm):
    class Meta:
        model = Collateral
        fields = [
            "name",
            "code",
            "category",
            "storages",
            "appraisal_value",
            "description",
            "photo",
            "intake_date",
            "notes",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Contoh: Cincin Emas 24K"}),
            "code": forms.TextInput(
                attrs={"placeholder": "Kosongkan agar dibuat otomatis"}
            ),
            "appraisal_value": forms.NumberInput(
                attrs={"step": "0.01", "placeholder": "Contoh: 5000000"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Tulis keterangan barang"}
            ),
            "photo": forms.FileInput(attrs={"accept": "image/*"}),
            "intake_date": DateInput(),
            "notes": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Catatan tambahan (opsional)"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["storages"].queryset = _active_storages()


class NewTransactionForm(BaseModelForm):
    class Meta:
        model = Transaction
        fields = [
            "nomor_kontrak",
            "status_kontrak",
            "scheme",
            "storages",
            "tanggal_pinjam",
            "tanggal_jatuh_tempo",
            "uang_pinjaman",
            "tujuan_pinjaman",
        ]
        widgets = {
            "nomor_kontrak": forms.TextInput(
                attrs={
                    "placeholder": "Kosongkan agar dibuat otomatis",
                    "autocomplete": "off",
                }
            ),
            "tanggal_pinjam": DateInput(),
            "tanggal_jatuh_tempo": DateInput(),
            "uang_pinjaman": forms.TextInput(
                attrs={
                    "inputmode": "numeric",
                    "autocomplete": "off",
                    "placeholder": "Contoh: 1000000",
                    "data-currency": "true",
                }
            ),
            "tujuan_pinjaman": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Contoh: Modal usaha dagang"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["scheme"].queryset = Scheme.objects.all()
        self.fields["storages"].queryset = _active_storages()
