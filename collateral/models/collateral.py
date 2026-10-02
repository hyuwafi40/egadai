from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from collateral.models.base import TimestampMixin
from collateral.utils.constants import (
    APPRAISAL_DECIMAL_PLACES,
    APPRAISAL_MAX_DIGITS,
    APPRAISAL_MAX_VALUE,
    COLLATERAL_PHOTO_UPLOAD_TO,
    DEFAULT_IS_ACTIVE,
    DEFAULT_STATUS,
    MAX_LENGTH_CODE,
    MAX_LENGTH_NAME,
    CollateralStatusChoices,
)
from collateral.utils.helpers import normalize_code, normalize_text
from collateral.utils.managers import ActiveManager
from collateral.utils.validators import (
    validate_image_extension,
    validate_image_size,
)


class Collateral(TimestampMixin):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        db_index=True,
        verbose_name="Nama Barang",
    )
    code = models.CharField(
        max_length=MAX_LENGTH_CODE,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
        verbose_name="Kode Barang",
        help_text="Kosongkan agar dibuat otomatis.",
    )
    category = models.ForeignKey(
        "vault.Category",
        on_delete=models.PROTECT,
        related_name="collaterals",
        verbose_name="Kategori",
    )
    storages = models.ForeignKey(
        "vault.Storages",
        on_delete=models.PROTECT,
        related_name="collaterals",
        verbose_name="Gudang",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Keterangan",
    )
    photo = models.ImageField(
        upload_to=COLLATERAL_PHOTO_UPLOAD_TO,
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_image_size],
        verbose_name="Foto Barang",
    )
    appraisal_value = models.DecimalField(
        max_digits=APPRAISAL_MAX_DIGITS,
        decimal_places=APPRAISAL_DECIMAL_PLACES,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(APPRAISAL_MAX_VALUE),
        ],
        verbose_name="Nilai Taksiran",
        help_text="Nilai taksiran barang dalam Rupiah.",
    )
    status = models.CharField(
        max_length=20,
        choices=CollateralStatusChoices.choices,
        default=DEFAULT_STATUS,
        db_index=True,
        verbose_name="Status",
    )
    intake_date = models.DateField(
        null=True,
        blank=True,
        verbose_name="Tanggal Masuk",
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
        verbose_name = "Barang Jaminan"
        verbose_name_plural = "Barang Jaminan"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)
        self.code = normalize_code(self.code) or None
        super().save(*args, **kwargs)

    def __str__(self):
        if self.code:
            return f"{self.name} [{self.code}]"
        return self.name
