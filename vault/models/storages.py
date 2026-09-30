from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from vault.models.base import TimestampMixin
from vault.utils.constants import (
    DEFAULT_IS_ACTIVE,
    DEFAULT_OCCUPANCY,
    LATITUDE_DECIMAL_PLACES,
    LATITUDE_MAX_DIGITS,
    LONGITUDE_DECIMAL_PLACES,
    LONGITUDE_MAX_DIGITS,
    MAX_LENGTH_CODE,
    MAX_LENGTH_NAME,
    MAX_LENGTH_PHONE,
    MAX_LENGTH_POSTAL_CODE,
    StorageStatusChoices,
)
from vault.utils.helpers import normalize_code, normalize_text
from vault.utils.managers import ActiveManager


class Storages(TimestampMixin):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        db_index=True,
    )
    kode_gudang = models.CharField(
        max_length=MAX_LENGTH_CODE,
        unique=True,
        db_index=True,
    )
    status = models.CharField(
        max_length=MAX_LENGTH_NAME,
        choices=StorageStatusChoices.choices,
        default=StorageStatusChoices.TERSEDIA,
        db_index=True,
    )
    address = models.TextField(blank=True)
    city = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=True,
        db_index=True,
    )
    province = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=True,
        db_index=True,
    )
    postal_code = models.CharField(
        max_length=MAX_LENGTH_POSTAL_CODE,
        blank=True,
    )
    phone = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        blank=True,
    )
    penanggung_jawab = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=True,
    )
    capacity = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    current_occupancy = models.PositiveIntegerField(
        default=DEFAULT_OCCUPANCY,
        validators=[MinValueValidator(0)],
    )
    latitude = models.DecimalField(
        max_digits=LATITUDE_MAX_DIGITS,
        decimal_places=LATITUDE_DECIMAL_PLACES,
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        max_digits=LONGITUDE_MAX_DIGITS,
        decimal_places=LONGITUDE_DECIMAL_PLACES,
        null=True,
        blank=True,
    )
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(
        default=DEFAULT_IS_ACTIVE,
        db_index=True,
    )

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        verbose_name = "Storages"
        verbose_name_plural = "Storages"
        ordering = ["name"]

    def clean(self):
        super().clean()
        if (
            self.capacity is not None
            and self.current_occupancy is not None
            and self.current_occupancy > self.capacity
        ):
            raise ValidationError(
                {
                    "current_occupancy": (
                        "Occupancy tidak boleh melebihi kapasitas gudang."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)
        self.kode_gudang = normalize_code(self.kode_gudang)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.kode_gudang})"
