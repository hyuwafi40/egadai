from django.core.exceptions import ValidationError

from collateral.utils.constants import (
    IMAGE_ALLOWED_EXTENSIONS,
    IMAGE_MAX_SIZE_BYTES,
)


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
