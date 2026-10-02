from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from vault.models.base import TimestampMixin
from vault.utils.constants import (
    BIAYA_ADMIN_DECIMAL_PLACES,
    BIAYA_ADMIN_MAX_DIGITS,
    BUNGA_DECIMAL_PLACES,
    BUNGA_MAX_DIGITS,
    BUNGA_MAX_VALUE,
    DENDA_DECIMAL_PLACES,
    DENDA_MAX_DIGITS,
    DURASI_MIN_VALUE,
    MAX_LENGTH_NAME,
    PeriodeBungaChoices,
)
from vault.utils.helpers import normalize_text
from vault.utils.validators import validate_denda_persen


class Scheme(TimestampMixin):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        unique=True,
        db_index=True,
        verbose_name="Nama Skema",
    )
    bunga = models.DecimalField(
        max_digits=BUNGA_MAX_DIGITS,
        decimal_places=BUNGA_DECIMAL_PLACES,
        validators=[MinValueValidator(0), MaxValueValidator(BUNGA_MAX_VALUE)],
        verbose_name="Bunga (%)",
        help_text="Dalam persen, dihitung per periode.",
    )
    periode_bunga = models.IntegerField(
        choices=PeriodeBungaChoices.choices,
        db_index=True,
        verbose_name="Periode Bunga",
    )
    durasi_maksimal_hari = models.PositiveIntegerField(
        validators=[MinValueValidator(DURASI_MIN_VALUE)],
        verbose_name="Durasi Maksimal",
        help_text="Dalam hari.",
    )
    denda_persen_perhari = models.DecimalField(
        max_digits=DENDA_MAX_DIGITS,
        decimal_places=DENDA_DECIMAL_PLACES,
        validators=[validate_denda_persen],
        verbose_name="Denda (% per hari)",
        help_text="Pilihan: 0.1, 0.2, 0.3, 0.4, 0.5.",
    )
    biaya_admin = models.DecimalField(
        max_digits=BIAYA_ADMIN_MAX_DIGITS,
        decimal_places=BIAYA_ADMIN_DECIMAL_PLACES,
        validators=[MinValueValidator(0)],
        verbose_name="Biaya Admin",
        help_text="Dalam Rupiah.",
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "Skema"
        verbose_name_plural = "Skema"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
