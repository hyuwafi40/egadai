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
    )
    nik = models.CharField(
        max_length=MAX_LENGTH_NIK,
        unique=True,
        db_index=True,
        validators=[validate_nik],
    )
    customer_code = models.CharField(
        max_length=MAX_LENGTH_CUSTOMER_CODE,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
    )
    photo = models.ImageField(
        upload_to=CUSTOMER_PHOTO_UPLOAD_TO,
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_image_size],
    )
    selfie = models.ImageField(
        upload_to=CUSTOMER_SELFIE_UPLOAD_TO,
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_image_size],
    )
    gender = models.CharField(
        max_length=20,
        choices=GenderChoices.choices,
        blank=True,
        db_index=True,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    occupation = models.CharField(
        max_length=MAX_LENGTH_OCCUPATION,
        blank=True,
    )
    marital_status = models.CharField(
        max_length=20,
        choices=MaritalStatusChoices.choices,
        blank=True,
    )
    phone = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        blank=True,
        validators=[validate_phone_id],
    )
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(
        max_length=MAX_LENGTH_CITY,
        blank=True,
        db_index=True,
    )
    province = models.CharField(
        max_length=MAX_LENGTH_PROVINCE,
        blank=True,
        db_index=True,
    )
    emergency_contact_name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=True,
    )
    emergency_contact_phone = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        blank=True,
        validators=[validate_phone_id],
    )
    emergency_contact_relationship = models.CharField(
        max_length=MAX_LENGTH_RELATIONSHIP,
        blank=True,
    )
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(
        default=DEFAULT_IS_ACTIVE,
        db_index=True,
    )

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)
        self.nik = normalize_nik(self.nik)
        self.customer_code = normalize_code(self.customer_code) or None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} [{self.nik}]"
