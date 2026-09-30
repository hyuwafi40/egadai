from django.db import models


class CompanyStatusChoices(models.TextChoices):
    PT = "pt", "PT"
    KOPERASI = "koperasi", "Koperasi"
    PERUM = "perum", "Perum"
    PERSERO = "persero", "Persero"


class CompanyTypeChoices(models.TextChoices):
    KONVENSIONAL = "konvensional", "Konvensional"
    SYARIAH = "syariah", "Syariah"


class BusinessScopeChoices(models.TextChoices):
    KABUPATEN_KOTA = "kabupaten_kota", "Kabupaten/Kota"
    PROVINSI = "provinsi", "Provinsi"
    NASIONAL = "nasional", "Nasional"


class PspTypeChoices(models.TextChoices):
    BADAN_HUKUM = "badan_hukum", "Badan Hukum"
    PERORANGAN = "perorangan", "Perorangan"


ALLOWED_URL_SCHEMES = ("http", "https")

MAX_LENGTH_SHORT = 50
MAX_LENGTH_MEDIUM = 100
MAX_LENGTH_LONG = 255
MAX_LENGTH_URL = 500
MAX_LENGTH_PHONE = 30
MAX_LENGTH_NPWP = 30
MAX_LENGTH_VERSION = 20

DEFAULT_BRAND_NAME = "Project Aplikasi"
DEFAULT_BRAND_DESCRIPTION = "Project Aplikasi"
DEFAULT_BRAND_VERSION = "1.0.0"
DEFAULT_BRAND_CREATOR = "Hamdayuwafii"
DEFAULT_BRAND_FACEBOOK = "https://facebook.com/hamdayuwafii"
DEFAULT_BRAND_INSTAGRAM = "https://instagram.com/hamdayuwafii"
DEFAULT_BRAND_TIKTOK = "https://www.tiktok.com/@hamdayuwafii"
DEFAULT_BRAND_YOUTUBE = "https://youtube.com/@hamdayuwafii"

DEFAULT_COUNTRY = "Indonesia"
DEFAULT_COMPANY_STATUS = CompanyStatusChoices.PT
DEFAULT_COMPANY_TYPE = CompanyTypeChoices.KONVENSIONAL
DEFAULT_BUSINESS_SCOPE = BusinessScopeChoices.KABUPATEN_KOTA
DEFAULT_PSP_TYPE = PspTypeChoices.BADAN_HUKUM

SEMVER_PATTERN = r"^\d+\.\d+\.\d+$"

CAPITAL_MAX_DIGITS = 20
CAPITAL_DECIMAL_PLACES = 2

LATITUDE_MAX_DIGITS = 9
LATITUDE_DECIMAL_PLACES = 6
LONGITUDE_MAX_DIGITS = 9
LONGITUDE_DECIMAL_PLACES = 6

BRAND_LOGO_UPLOAD_TO = "brand/logo/%Y/%m/"
ORG_LOGO_UPLOAD_TO = "orgs/logo/%Y/%m/"
IMAGE_ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png", "webp")
IMAGE_MAX_SIZE_BYTES = 2 * 1024 * 1024

SINGLETON_CACHE_PREFIX = "core"
SINGLETON_CACHE_SUFFIX = "singleton"

SINGLETON_AUTO_FIELDS = ("id", "pk", "created_at", "updated_at")

FALLBACK_APP_NAME = "Egadai"
