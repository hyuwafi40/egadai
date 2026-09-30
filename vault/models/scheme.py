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
    )
    bunga = models.DecimalField(
        max_digits=BUNGA_MAX_DIGITS,
        decimal_places=BUNGA_DECIMAL_PLACES,
        validators=[MinValueValidator(0), MaxValueValidator(BUNGA_MAX_VALUE)],
    )
    periode_bunga = models.IntegerField(
        choices=PeriodeBungaChoices.choices,
        db_index=True,
    )
    durasi_maksimal_hari = models.PositiveIntegerField(
        validators=[MinValueValidator(DURASI_MIN_VALUE)],
    )
    denda_persen_perhari = models.DecimalField(
        max_digits=DENDA_MAX_DIGITS,
        decimal_places=DENDA_DECIMAL_PLACES,
        validators=[validate_denda_persen],
    )
    biaya_admin = models.DecimalField(
        max_digits=BIAYA_ADMIN_MAX_DIGITS,
        decimal_places=BIAYA_ADMIN_DECIMAL_PLACES,
        validators=[MinValueValidator(0)],
    )

    objects = models.Manager()

    class Meta:
        verbose_name = "Scheme"
        verbose_name_plural = "Schemes"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
