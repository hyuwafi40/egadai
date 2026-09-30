from decimal import Decimal, InvalidOperation

from django.core.exceptions import ValidationError

from vault.utils.constants import DENDA_PERSEN_VALUES


def validate_denda_persen(value):
    if value is None:
        return
    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, ValueError, TypeError):
        raise ValidationError("Denda persen per hari harus berupa angka.")
    allowed = [Decimal(str(v)) for v in DENDA_PERSEN_VALUES]
    if decimal_value not in allowed:
        raise ValidationError(
            "Denda persen per hari harus salah satu dari: "
            + ", ".join(str(v) for v in DENDA_PERSEN_VALUES)
            + "."
        )
