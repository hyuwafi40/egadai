from django.db import models


class GenderChoices(models.TextChoices):
    MALE = "male", "Laki-laki"
    FEMALE = "female", "Perempuan"


class MaritalStatusChoices(models.TextChoices):
    SINGLE = "single", "Belum Menikah"
    MARRIED = "married", "Menikah"
    DIVORCED = "divorced", "Cerai"
    WIDOWED = "widowed", "Janda/Duda"


MAX_LENGTH_NAME = 100
MAX_LENGTH_NIK = 16
MAX_LENGTH_CUSTOMER_CODE = 20
MAX_LENGTH_PHONE = 20
MAX_LENGTH_CITY = 100
MAX_LENGTH_PROVINCE = 100
MAX_LENGTH_RELATIONSHIP = 50
MAX_LENGTH_OCCUPATION = 100

NIK_MIN_LENGTH = 13
NIK_MAX_LENGTH = 16

PHONE_COUNTRY_CODE_ID = "+62"
PHONE_LOCAL_PREFIX_ID = "0"
PHONE_MIN_LENGTH = 10
PHONE_MAX_LENGTH = 15

CUSTOMER_PHOTO_UPLOAD_TO = "customers/ktp/%Y/%m/"
CUSTOMER_SELFIE_UPLOAD_TO = "customers/selfie/%Y/%m/"
IMAGE_ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png", "webp")
IMAGE_MAX_SIZE_BYTES = 2 * 1024 * 1024

DEFAULT_IS_ACTIVE = True
