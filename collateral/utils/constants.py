from django.db import models


class CollateralStatusChoices(models.TextChoices):
    STORED = "stored", "Tersimpan"
    REDEEMED = "redeemed", "Ditebus"
    AUCTIONED = "auctioned", "Dilelang"


MAX_LENGTH_NAME = 200
MAX_LENGTH_CODE = 20

APPRAISAL_MAX_DIGITS = 15
APPRAISAL_DECIMAL_PLACES = 2
APPRAISAL_MAX_VALUE = 10**12

COLLATERAL_PHOTO_UPLOAD_TO = "collaterals/photo/%Y/%m/"
IMAGE_ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png", "webp")
IMAGE_MAX_SIZE_BYTES = 2 * 1024 * 1024

DEFAULT_IS_ACTIVE = True
DEFAULT_STATUS = CollateralStatusChoices.STORED

COLLATERALS_PER_PAGE = 10
