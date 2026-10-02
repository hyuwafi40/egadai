from django.db import models


class PaymentTypeChoices(models.TextChoices):
    CICILAN = "cicilan", "Cicilan"
    LUNAS = "lunas", "Lunas"


class PaymentMethodChoices(models.TextChoices):
    CASH = "cash", "Tunai"
    TRANSFER = "transfer", "Transfer"


MAX_LENGTH_PAYMENT_NUMBER = 36
MAX_LENGTH_CHOICE = 20

PAYMENT_NUMBER_PREFIX = "PAY"
PAYMENT_NUMBER_LENGTH = 8

JUMLAH_BAYAR_MAX_DIGITS = 15
JUMLAH_BAYAR_DECIMAL_PLACES = 2
JUMLAH_BAYAR_MIN_VALUE = 0

DEFAULT_PAYMENT_TYPE = PaymentTypeChoices.CICILAN
DEFAULT_PAYMENT_METHOD = PaymentMethodChoices.CASH

PAYMENTS_PER_PAGE = 10
