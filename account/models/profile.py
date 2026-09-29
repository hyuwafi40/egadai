from django.conf import settings
from django.db import models

from account.models.base import TimestampMixin
from account.utils.constants import (
    DEFAULT_COUNTRY,
    MAX_LENGTH_MEDIUM,
    MAX_LENGTH_PHONE,
    MAX_LENGTH_SHORT,
    MAX_LENGTH_URL,
    PROFILE_PHOTO_UPLOAD_TO,
    EmploymentTypeChoices,
    GenderChoices,
    MaritalStatusChoices,
)
from account.utils.validators import (
    validate_image_extension,
    validate_image_size,
    validate_phone_id,
)


class Profile(TimestampMixin):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    employee_id = models.CharField(
        max_length=MAX_LENGTH_SHORT,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
    )
    full_name = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        blank=True,
    )
    nickname = models.CharField(
        max_length=MAX_LENGTH_SHORT,
        blank=True,
    )
    photo = models.ImageField(
        upload_to=PROFILE_PHOTO_UPLOAD_TO,
        max_length=MAX_LENGTH_URL,
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_image_size],
    )
    gender = models.CharField(
        max_length=MAX_LENGTH_SHORT,
        choices=GenderChoices.choices,
        blank=True,
    )
    date_of_birth = models.DateField(null=True, blank=True)
    place_of_birth = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        blank=True,
    )
    marital_status = models.CharField(
        max_length=MAX_LENGTH_SHORT,
        choices=MaritalStatusChoices.choices,
        blank=True,
    )
    religion = models.CharField(
        max_length=MAX_LENGTH_SHORT,
        blank=True,
    )
    phone = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        blank=True,
        validators=[validate_phone_id],
    )
    address = models.TextField(blank=True)
    city = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        blank=True,
    )
    province = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        blank=True,
    )
    postal_code = models.CharField(
        max_length=MAX_LENGTH_SHORT,
        blank=True,
    )
    country = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        blank=True,
        default=DEFAULT_COUNTRY,
    )
    department = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        blank=True,
        db_index=True,
    )
    position = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        blank=True,
    )
    employment_type = models.CharField(
        max_length=MAX_LENGTH_SHORT,
        choices=EmploymentTypeChoices.choices,
        blank=True,
    )
    hire_date = models.DateField(null=True, blank=True)
    emergency_contact_name = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        blank=True,
    )
    emergency_contact_phone = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        blank=True,
        validators=[validate_phone_id],
    )
    about = models.TextField(blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name or self.user.username
