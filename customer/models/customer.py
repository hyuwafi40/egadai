from django.db import models

from customer.models.base import TimestampMixin
from customer.utils.constants import (
    CUSTOMER_PHOTO_UPLOAD_TO,
    CUSTOMER_SELFIE_UPLOAD_TO,
    DEFAULT_IS_ACTIVE,
    MAX_LENGTH_CITY,
    MAX_LENGTH_CUSTOMER_CODE,
    MAX_LENGTH_NIK,
    MAX_LENGTH_NAME,
    MAX_LENGTH_OCCUPATION,
    MAX_LENGTH_PHONE,
    MAX_LENGTH_PROVINCE,
    MAX_LENGTH_RELATIONSHIP,
    GenderChoices,
    MaritalStatusChoices,
)
from customer.utils.helpers import (
    normalize_code,
    normalize_nik,
    normalize_text,
)
from customer.utils.managers import ActiveManager
from customer.utils.validators import (
    validate_image_extension,
    validate_image_size,
    validate_nik,
    validate_phone_id,
)


class Customer(TimestampMixin):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        db_index=True,
        verbose_name="Nama Lengkap",
    )
    nik = models.CharField(
        max_length=MAX_LENGTH_NIK,
        unique=True,
        db_index=True,
        validators=[validate_nik],
        verbose_name="NIK",
        help_text="16 angka sesuai KTP.",
    )
    customer_code = models.CharField(
        max_length=MAX_LENGTH_CUSTOMER_CODE,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        verbose_name="Kode Nasabah",
        help_text="Kosongkan agar dibuat otomatis.",
    )
    photo = models.ImageField(
        upload_to=CUSTOMER_PHOTO_UPLOAD_TO,
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_image_size],
        verbose_name="Foto KTP",
    )
    selfie = models.ImageField(
        upload_to=CUSTOMER_SELFIE_UPLOAD_TO,
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_image_size],
        verbose_name="Foto Selfie",
    )
    gender = models.CharField(
        max_length=20,
        choices=GenderChoices.choices,
        blank=True,
        db_index=True,
        verbose_name="Jenis Kelamin",
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        verbose_name="Tanggal Lahir",
    )
    occupation = models.CharField(
        max_length=MAX_LENGTH_OCCUPATION,
        blank=True,
        verbose_name="Pekerjaan",
    )
    marital_status = models.CharField(
        max_length=20,
        choices=MaritalStatusChoices.choices,
        blank=True,
        verbose_name="Status Pernikahan",
    )
    phone = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        blank=True,
        validators=[validate_phone_id],
        verbose_name="Nomor HP",
    )
    email = models.EmailField(
        blank=True,
        verbose_name="Email",
    )
    address = models.TextField(
        blank=True,
        verbose_name="Alamat",
    )
    city = models.CharField(
        max_length=MAX_LENGTH_CITY,
        blank=True,
        db_index=True,
        verbose_name="Kota",
    )
    province = models.CharField(
        max_length=MAX_LENGTH_PROVINCE,
        blank=True,
        db_index=True,
        verbose_name="Provinsi",
    )
    emergency_contact_name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=True,
        verbose_name="Nama Kontak Darurat",
    )
    emergency_contact_phone = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        blank=True,
        validators=[validate_phone_id],
        verbose_name="HP Kontak Darurat",
    )
    emergency_contact_relationship = models.CharField(
        max_length=MAX_LENGTH_RELATIONSHIP,
        blank=True,
        verbose_name="Hubungan",
        help_text="Contoh: Istri, Suami, Ayah, Ibu, Saudara.",
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Catatan",
    )
    is_active = models.BooleanField(
        default=DEFAULT_IS_ACTIVE,
        db_index=True,
        verbose_name="Aktif",
    )

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        verbose_name = "Nasabah"
        verbose_name_plural = "Nasabah"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)
        self.nik = normalize_nik(self.nik)
        self.customer_code = normalize_code(self.customer_code) or None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} [{self.nik}]"
