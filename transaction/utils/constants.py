from django.db import models


class ContractStatusChoices(models.TextChoices):
    AKTIF = "aktif", "Aktif"
    LUNAS = "lunas", "Lunas"
    JATUH_TEMPO = "jatuh_tempo", "Jatuh Tempo"
    LELANG = "lelang", "Lelang"


MAX_LENGTH_CONTRACT_NUMBER = 36
MAX_LENGTH_STATUS = 20

UANG_PINJAMAN_MAX_DIGITS = 15
UANG_PINJAMAN_DECIMAL_PLACES = 2
UANG_PINJAMAN_MIN_VALUE = 0

CONTRACT_NUMBER_PREFIX = "TRX"
CONTRACT_NUMBER_LENGTH = 8

DEFAULT_STATUS = ContractStatusChoices.AKTIF

TRANSACTIONS_PER_PAGE = 10
