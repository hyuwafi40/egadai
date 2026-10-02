import uuid

from transaction.utils.constants import (
    CONTRACT_NUMBER_LENGTH,
    CONTRACT_NUMBER_PREFIX,
)


def normalize_text(value):
    if not value:
        return value
    return value.strip()


def normalize_contract_number(value):
    if not value:
        return value
    return value.strip().upper()


def generate_contract_number():
    raw = uuid.uuid4().hex.upper()
    short = raw[:CONTRACT_NUMBER_LENGTH]
    return f"{CONTRACT_NUMBER_PREFIX}-{short}"
