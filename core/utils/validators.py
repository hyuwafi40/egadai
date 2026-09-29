import re

from django.core.exceptions import ValidationError

from core.utils.constants import (
    ALLOWED_URL_SCHEMES,
    IMAGE_ALLOWED_EXTENSIONS,
    IMAGE_MAX_SIZE_BYTES,
    SEMVER_PATTERN,
)


def validate_url_scheme(value):
    if not value:
        return
    if "://" not in value:
        raise ValidationError("URL harus menyertakan skema http atau https.")
    scheme = value.split("://", 1)[0].lower()
    if scheme not in ALLOWED_URL_SCHEMES:
        raise ValidationError("URL harus menggunakan skema http atau https.")


def validate_semver(value):
    if not value:
        return
    if not re.match(SEMVER_PATTERN, value):
        raise ValidationError("Format versi harus mengikuti pola X.Y.Z.")


def validate_image_extension(value):
    if not value:
        return
    name = getattr(value, "name", "")
    if "." not in name:
        raise ValidationError("File gambar harus memiliki ekstensi.")
    ext = name.rsplit(".", 1)[-1].lower()
    if ext not in IMAGE_ALLOWED_EXTENSIONS:
        allowed = ", ".join(IMAGE_ALLOWED_EXTENSIONS)
        raise ValidationError(f"Ekstensi gambar tidak didukung. Gunakan: {allowed}.")


def validate_image_size(value):
    if not value:
        return
    size = getattr(value, "size", 0)
    if size > IMAGE_MAX_SIZE_BYTES:
        max_mb = IMAGE_MAX_SIZE_BYTES / (1024 * 1024)
        raise ValidationError(f"Ukuran gambar maksimal {max_mb:.0f} MB.")
