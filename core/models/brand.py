from django.db import models
from solo.models import SingletonModel

from core.models.base import TimestampMixin
from core.utils.constants import (
    BRAND_LOGO_UPLOAD_TO,
    DEFAULT_BRAND_CREATOR,
    DEFAULT_BRAND_DESCRIPTION,
    DEFAULT_BRAND_FACEBOOK,
    DEFAULT_BRAND_INSTAGRAM,
    DEFAULT_BRAND_NAME,
    DEFAULT_BRAND_TIKTOK,
    DEFAULT_BRAND_VERSION,
    DEFAULT_BRAND_YOUTUBE,
    MAX_LENGTH_LONG,
    MAX_LENGTH_MEDIUM,
    MAX_LENGTH_URL,
    MAX_LENGTH_VERSION,
)
from core.utils.helpers import normalize_text, normalize_url
from core.utils.managers import SingletonManager
from core.utils.validators import (
    validate_image_extension,
    validate_image_size,
    validate_semver,
    validate_url_scheme,
)


class Brand(TimestampMixin, SingletonModel):
    name = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        default=DEFAULT_BRAND_NAME,
    )
    description = models.TextField(
        default=DEFAULT_BRAND_DESCRIPTION,
    )
    version = models.CharField(
        max_length=MAX_LENGTH_VERSION,
        default=DEFAULT_BRAND_VERSION,
        validators=[validate_semver],
    )
    creator = models.CharField(
        max_length=MAX_LENGTH_LONG,
        default=DEFAULT_BRAND_CREATOR,
    )
    facebook = models.URLField(
        max_length=MAX_LENGTH_URL,
        default=DEFAULT_BRAND_FACEBOOK,
        validators=[validate_url_scheme],
    )
    instagram = models.URLField(
        max_length=MAX_LENGTH_URL,
        default=DEFAULT_BRAND_INSTAGRAM,
        validators=[validate_url_scheme],
    )
    tiktok = models.URLField(
        max_length=MAX_LENGTH_URL,
        default=DEFAULT_BRAND_TIKTOK,
        validators=[validate_url_scheme],
    )
    youtube = models.URLField(
        max_length=MAX_LENGTH_URL,
        default=DEFAULT_BRAND_YOUTUBE,
        validators=[validate_url_scheme],
    )
    logo = models.ImageField(
        upload_to=BRAND_LOGO_UPLOAD_TO,
        max_length=MAX_LENGTH_URL,
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_image_size],
    )

    objects = SingletonManager()

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brand"

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)
        self.creator = normalize_text(self.creator)
        self.facebook = normalize_url(self.facebook)
        self.instagram = normalize_url(self.instagram)
        self.tiktok = normalize_url(self.tiktok)
        self.youtube = normalize_url(self.youtube)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
