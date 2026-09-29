from django.db import models
from solo.models import SingletonModel

from core.models.base import TimestampMixin
from core.utils.constants import (
    CAPITAL_DECIMAL_PLACES,
    CAPITAL_MAX_DIGITS,
    DEFAULT_BUSINESS_SCOPE,
    DEFAULT_COMPANY_STATUS,
    DEFAULT_COMPANY_TYPE,
    DEFAULT_COUNTRY,
    DEFAULT_PSP_TYPE,
    LATITUDE_DECIMAL_PLACES,
    LATITUDE_MAX_DIGITS,
    LONGITUDE_DECIMAL_PLACES,
    LONGITUDE_MAX_DIGITS,
    MAX_LENGTH_LONG,
    MAX_LENGTH_MEDIUM,
    MAX_LENGTH_NPWP,
    MAX_LENGTH_PHONE,
    MAX_LENGTH_SHORT,
    MAX_LENGTH_URL,
    ORG_LOGO_UPLOAD_TO,
    BusinessScopeChoices,
    CompanyStatusChoices,
    CompanyTypeChoices,
    PspTypeChoices,
)
from core.utils.helpers import normalize_text, normalize_url
from core.utils.managers import SingletonManager
from core.utils.validators import (
    validate_image_extension,
    validate_image_size,
    validate_url_scheme,
)


class Orgs(TimestampMixin, SingletonModel):
    name = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        default="",
        blank=True,
    )
    owner = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        default="",
        blank=True,
    )
    logo = models.ImageField(
        upload_to=ORG_LOGO_UPLOAD_TO,
        max_length=MAX_LENGTH_URL,
        blank=True,
        null=True,
        validators=[validate_image_extension, validate_image_size],
    )
    legal_name = models.CharField(
        max_length=MAX_LENGTH_LONG,
        blank=True,
    )
    brand_name = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        blank=True,
    )
    company_status = models.CharField(
        max_length=MAX_LENGTH_SHORT,
        choices=CompanyStatusChoices.choices,
        default=DEFAULT_COMPANY_STATUS,
    )
    company_type = models.CharField(
        max_length=MAX_LENGTH_SHORT,
        choices=CompanyTypeChoices.choices,
        default=DEFAULT_COMPANY_TYPE,
    )
    description = models.TextField(blank=True)
    tagline = models.CharField(
        max_length=MAX_LENGTH_LONG,
        blank=True,
    )
    npwp = models.CharField(
        max_length=MAX_LENGTH_NPWP,
        blank=True,
    )
    license_number = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        blank=True,
    )
    license_date = models.DateField(null=True, blank=True)
    deed_number = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        blank=True,
    )
    deed_date = models.DateField(null=True, blank=True)
    last_amendment_number = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        blank=True,
    )
    last_amendment_date = models.DateField(null=True, blank=True)
    founded_date = models.DateField(null=True, blank=True)
    founded_place = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        blank=True,
    )
    business_sector = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        blank=True,
    )
    authorized_capital = models.DecimalField(
        max_digits=CAPITAL_MAX_DIGITS,
        decimal_places=CAPITAL_DECIMAL_PLACES,
        null=True,
        blank=True,
    )
    paid_up_capital = models.DecimalField(
        max_digits=CAPITAL_MAX_DIGITS,
        decimal_places=CAPITAL_DECIMAL_PLACES,
        null=True,
        blank=True,
    )
    business_scope = models.CharField(
        max_length=MAX_LENGTH_SHORT,
        choices=BusinessScopeChoices.choices,
        default=DEFAULT_BUSINESS_SCOPE,
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
    phone = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        blank=True,
    )
    fax = models.CharField(
        max_length=MAX_LENGTH_PHONE,
        blank=True,
    )
    email = models.EmailField(blank=True)
    website = models.URLField(
        max_length=MAX_LENGTH_URL,
        blank=True,
        validators=[validate_url_scheme],
    )
    business_type = models.CharField(
        max_length=MAX_LENGTH_MEDIUM,
        blank=True,
    )
    products_services = models.TextField(blank=True)
    total_branches = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    total_employees = models.PositiveIntegerField(
        null=True,
        blank=True,
    )
    psp_name = models.CharField(
        max_length=MAX_LENGTH_LONG,
        blank=True,
    )
    psp_type = models.CharField(
        max_length=MAX_LENGTH_SHORT,
        choices=PspTypeChoices.choices,
        default=DEFAULT_PSP_TYPE,
    )
    vision = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    latitude = models.DecimalField(
        max_digits=LATITUDE_MAX_DIGITS,
        decimal_places=LATITUDE_DECIMAL_PLACES,
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        max_digits=LONGITUDE_MAX_DIGITS,
        decimal_places=LONGITUDE_DECIMAL_PLACES,
        null=True,
        blank=True,
    )

    objects = SingletonManager()

    class Meta:
        verbose_name = "Orgs"
        verbose_name_plural = "Orgs"

    def save(self, *args, **kwargs):
        self.name = normalize_text(self.name)
        self.owner = normalize_text(self.owner)
        self.website = normalize_url(self.website)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or "Orgs"
