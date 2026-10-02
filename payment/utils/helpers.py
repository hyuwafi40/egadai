import uuid

from payment.utils.constants import (
    PAYMENT_NUMBER_LENGTH,
    PAYMENT_NUMBER_PREFIX,
)


def normalize_text(value):
    if not value:
        return value
    return value.strip()


def normalize_payment_number(value):
    if not value:
        return value
    return value.strip().upper()


def generate_payment_number():
    raw = uuid.uuid4().hex.upper()
    short = raw[:PAYMENT_NUMBER_LENGTH]
    return f"{PAYMENT_NUMBER_PREFIX}-{short}"
