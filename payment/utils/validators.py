from django.core.exceptions import ValidationError

from payment.utils.constants import (
    MAX_LENGTH_PAYMENT_NUMBER,
    PAYMENT_NUMBER_PREFIX,
)


def validate_payment_number(value):
    if not value:
        return
    if len(value) > MAX_LENGTH_PAYMENT_NUMBER:
        raise ValidationError(
            f"Panjang nomor pembayaran maksimal {MAX_LENGTH_PAYMENT_NUMBER} karakter."
        )
    if not value.startswith(f"{PAYMENT_NUMBER_PREFIX}-"):
        raise ValidationError(
            f"Nomor pembayaran harus diawali dengan '{PAYMENT_NUMBER_PREFIX}-'."
        )
