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
        verbose_name="Nama Gudang",
    )
    kode_gudang = models.CharField(
        max_length=MAX_LENGTH_CODE,
        unique=True,
        db_index=True,
        verbose_name="Kode Gudang",
    )
    status = models.CharField(
        max_length=MAX_LENGTH_NAME,
        choices=StorageStatusChoices.choices,
        default=StorageStatusChoices.TERSEDIA,
        db_index=True,
        verbose_name="Status",
    )
    address = models.TextField(
        blank=True,
        verbose_name="Alamat",
    )
    city = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=True,
        db_index=True,
        verbose_name="Kota",
    )
    province = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=True,
        db_index=True,
        verbose_name="Provinsi",
    )
    postal_code = models.CharField(
        max_length=MAX_LENGTH_POSTAL_CODE,
        blank=True,
        verbose_name="Kode Pos",
    )
    phone = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        blank=True,
        verbose_name="Nomor HP",
    )
    penanggung_jawab = models.CharField(
        max_length=MAX_LENGTH_NAME,
        blank=True,
        verbose_name="Petugas",
    )
    capacity = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Kapasitas",
    )
    current_occupancy = models.PositiveIntegerField(
        default=DEFAULT_OCCUPANCY,
        validators=[MinValueValidator(0)],
        verbose_name="Terisi",
    )
    latitude = models.DecimalField(
        max_digits=LATITUDE_MAX_DIGITS,
        decimal_places=LATITUDE_DECIMAL_PLACES,
        null=True,
        blank=True,
        verbose_name="Latitude",
    )
    longitude = models.DecimalField(
        max_digits=LONGITUDE_MAX_DIGITS,
        decimal_places=LONGITUDE_DECIMAL_PLACES,
        null=True,
        blank=True,
        verbose_name="Longitude",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Keterangan",
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
        verbose_name = "Gudang"
        verbose_name_plural = "Gudang"
        ordering = ["name"]

    def clean(self):
        super().clean()
        if (
            self.capacity is not None
            and self.current_occupancy is not None
            and self.current_occupancy > self.capacity
        ):
            raise ValidationError(
                {"current_occupancy": ("Jumlah terisi tidak boleh melebihi kapasitas.")}
            )

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)
        self.kode_gudang = normalize_code(self.kode_gudang)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.kode_gudang})"
