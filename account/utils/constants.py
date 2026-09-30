from django.db import models


class JobChoices(models.TextChoices):
    DEVELOPER = "developer", "Developer"
    ADMINISTRATOR = "administrator", "Administrator"
    REGULER = "reguler", "Reguler"


class GenderChoices(models.TextChoices):
    MALE = "male", "Laki-laki"
    FEMALE = "female", "Perempuan"


class MaritalStatusChoices(models.TextChoices):
    SINGLE = "single", "Belum Menikah"
    MARRIED = "married", "Menikah"
    DIVORCED = "divorced", "Cerai"
    WIDOWED = "widowed", "Janda/Duda"


class EmploymentTypeChoices(models.TextChoices):
    PERMANENT = "permanent", "Tetap"
    CONTRACT = "contract", "Kontrak"
    PROBATION = "probation", "Percobaan"
    INTERN = "intern", "Magang"


MAX_LENGTH_USERNAME = 150
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_JOB = 20
MAX_LENGTH_SHORT = 50
MAX_LENGTH_MEDIUM = 100
MAX_LENGTH_URL = 500
MAX_LENGTH_PHONE = 20

DEFAULT_COUNTRY = "Indonesia"
DEFAULT_JOB = JobChoices.REGULER
DEFAULT_PASSWORD = "anggota123"
USERS_PER_PAGE = 10

PHONE_COUNTRY_CODE_ID = "+62"
PHONE_LOCAL_PREFIX_ID = "0"
PHONE_MIN_LENGTH = 10
PHONE_MAX_LENGTH = 15

PROFILE_PHOTO_UPLOAD_TO = "profiles/photo/%Y/%m/"
IMAGE_ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png", "webp")
IMAGE_MAX_SIZE_BYTES = 2 * 1024 * 1024

ROLE_DEVELOPER_FLAGS = {
    "is_active": True,
    "is_staff": True,
    "is_superuser": True,
}

ROLE_ADMINISTRATOR_FLAGS = {
    "is_active": True,
    "is_staff": True,
    "is_superuser": False,
}

ROLE_REGULER_FLAGS = {
    "is_active": True,
    "is_staff": False,
    "is_superuser": False,
}

ROLE_FLAGS_MAP = {
    JobChoices.DEVELOPER: ROLE_DEVELOPER_FLAGS,
    JobChoices.ADMINISTRATOR: ROLE_ADMINISTRATOR_FLAGS,
    JobChoices.REGULER: ROLE_REGULER_FLAGS,
}

ROLE_FLAG_FIELDS = ("is_active", "is_staff", "is_superuser")
