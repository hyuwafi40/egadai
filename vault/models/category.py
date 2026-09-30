from django.db import models

from vault.models.base import TimestampMixin
from vault.utils.constants import (
    DEFAULT_IS_ACTIVE,
    DEFAULT_ORDER,
    MAX_LENGTH_CODE,
    MAX_LENGTH_ICON,
    MAX_LENGTH_NAME,
)
from vault.utils.helpers import normalize_code, normalize_text
from vault.utils.managers import ActiveManager


class Category(TimestampMixin):
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
    icon = models.CharField(
        max_length=MAX_LENGTH_ICON,
        blank=True,
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
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["order", "name"]

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)
        self.code = normalize_code(self.code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} [{self.code}]"
