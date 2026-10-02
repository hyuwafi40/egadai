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
    )
    code = models.CharField(
        max_length=MAX_LENGTH_CODE,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
    )
    owner = models.ForeignKey(
        "customer.Customer",
        on_delete=models.PROTECT,
        related_name="collaterals",
    )
    category = models.ForeignKey(
        "vault.Category",
        on_delete=models.PROTECT,
        related_name="collaterals",
    )
    storages = models.ForeignKey(
        "vault.Storages",
        on_delete=models.PROTECT,
        related_name="collaterals",
    )
    description = models.TextField(blank=True)
    photo = models.ImageField(
        upload_to=COLLATERAL_PHOTO_UPLOAD_TO,
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_image_size],
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
    )
    status = models.CharField(
        max_length=20,
        choices=CollateralStatusChoices.choices,
        default=DEFAULT_STATUS,
        db_index=True,
    )
    intake_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    is_active = models.BooleanField(
        default=DEFAULT_IS_ACTIVE,
        db_index=True,
    )

    objects = models.Manager()
    active = ActiveManager()

    class Meta:
        verbose_name = "Collateral"
        verbose_name_plural = "Collaterals"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)
        self.code = normalize_code(self.code) or None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.owner.name}"
