from django.db import models

from vault.models.base import TimestampMixin
from vault.utils.constants import (
    MAX_LENGTH_CODE,
    MAX_LENGTH_NAME,
)
from vault.utils.helpers import normalize_code, normalize_text


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
    description = models.TextField(blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)
        self.code = normalize_code(self.code)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} [{self.code}]"
