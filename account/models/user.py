from django.contrib.auth.models import AbstractUser
from django.db import models

from account.models.base import TimestampMixin
from account.utils.constants import (
    DEFAULT_JOB,
    MAX_LENGTH_EMAIL,
    MAX_LENGTH_JOB,
    ROLE_FLAGS_MAP,
    ROLE_FLAG_FIELDS,
    JobChoices,
)
from account.utils.helpers import (
    normalize_email,
    normalize_username,
)
from account.utils.managers import UserManager


class User(TimestampMixin, AbstractUser):
    email = models.EmailField(
        max_length=MAX_LENGTH_EMAIL,
        unique=True,
    )
    job = models.CharField(
        max_length=MAX_LENGTH_JOB,
        choices=JobChoices.choices,
        default=DEFAULT_JOB,
        db_index=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        self.email = normalize_email(self.email)
        self.username = normalize_username(self.username)
        self.job = self.job or DEFAULT_JOB
        flags = ROLE_FLAGS_MAP.get(self.job)
        if not flags:
            raise ValueError(f"Job tidak valid: {self.job}")
        self.is_active = flags["is_active"]
        self.is_staff = flags["is_staff"]
        self.is_superuser = flags["is_superuser"]
        update_fields = kwargs.get("update_fields")
        if update_fields is not None:
            update_fields = set(update_fields)
            update_fields.update(ROLE_FLAG_FIELDS)
            kwargs["update_fields"] = list(update_fields)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
