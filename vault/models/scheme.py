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
    CAPITAL_DECIMAL_PLACES,
    CAPITAL_MAX_DIGITS,
    DEFAULT_IS_ACTIVE,
    DEFAULT_IS_DEFAULT,
    DEFAULT_ORDER,
    DENDA_DECIMAL_PLACES,
    DENDA_MAX_DIGITS,
    DURASI_MIN_VALUE,
    LTV_DECIMAL_PLACES,
    LTV_MAX_DIGITS,
    LTV_MAX_VALUE,
    MAX_LENGTH_CODE,
    MAX_LENGTH_NAME,
    PeriodeBungaChoices,
)
from vault.utils.helpers import normalize_code, normalize_text
from vault.utils.managers import ActiveManager
from vault.utils.validators import validate_denda_persen


class Scheme(TimestampMixin):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        unique=True,
        db_index=True,
    )
    code = models.CharField(
        max_length=MAX_LENGTH_CODE,
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
    min_pinjaman = models.DecimalField(
        max_digits=CAPITAL_MAX_DIGITS,
        decimal_places=CAPITAL_DECIMAL_PLACES,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    max_pinjaman = models.DecimalField(
        max_digits=CAPITAL_MAX_DIGITS,
        decimal_places=CAPITAL_DECIMAL_PLACES,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
    )
    ltv_persen = models.DecimalField(
        max_digits=LTV_MAX_DIGITS,
        decimal_places=LTV_DECIMAL_PLACES,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(LTV_MAX_VALUE)],
    )
    perpanjangan_bunga_persen = models.DecimalField(
        max_digits=BUNGA_MAX_DIGITS,
        decimal_places=BUNGA_DECIMAL_PLACES,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(BUNGA_MAX_VALUE)],
    )
    is_default = models.BooleanField(
        default=DEFAULT_IS_DEFAULT,
        db_index=True,
    )
    order = models.PositiveIntegerField(
        default=DEFAULT_ORDER,
        db_index=True,
    )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(
        default=DEFAULT_IS_ACTIVE,
        db_index=True,
    )

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        verbose_name = "Scheme"
        verbose_name_plural = "Schemes"
        ordering = ["order", "name"]

    def clean(self):
        super().clean()
        if (
            self.min_pinjaman is not None
            and self.max_pinjaman is not None
            and self.min_pinjaman > self.max_pinjaman
        ):
            raise ValidationError(
                {
                    "max_pinjaman": (
                        "Max pinjaman harus lebih besar atau sama "
                        "dengan min pinjaman."
                    )
                }
            )

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)
        self.code = normalize_code(self.code)
        if self.is_default and self.pk:
            Scheme.objects.filter(
                is_default=True,
            ).exclude(
                pk=self.pk
            ).update(is_default=False)
        elif self.is_default and not self.pk:
            Scheme.objects.filter(is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} [{self.code}]"
