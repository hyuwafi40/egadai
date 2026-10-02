from django.core.exceptions import ValidationError

from transaction.utils.constants import (
    CONTRACT_NUMBER_PREFIX,
    MAX_LENGTH_CONTRACT_NUMBER,
)


def validate_contract_number(value):
    if not value:
        return
    if len(value) > MAX_LENGTH_CONTRACT_NUMBER:
        raise ValidationError(
            f"Panjang nomor kontrak maksimal {MAX_LENGTH_CONTRACT_NUMBER} karakter."
        )
    if not value.startswith(f"{CONTRACT_NUMBER_PREFIX}-"):
        raise ValidationError(
            f"Nomor kontrak harus diawali dengan '{CONTRACT_NUMBER_PREFIX}-'."
        )
