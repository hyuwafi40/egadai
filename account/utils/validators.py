from django.core.exceptions import ValidationError

from account.utils.constants import (
    IMAGE_ALLOWED_EXTENSIONS,
    IMAGE_MAX_SIZE_BYTES,
    PHONE_COUNTRY_CODE_ID,
    PHONE_LOCAL_PREFIX_ID,
    PHONE_MAX_LENGTH,
    PHONE_MIN_LENGTH,
)


def validate_phone_id(value):
    if not value:
        return
    cleaned = value.replace(" ", "").replace("-", "")
    if cleaned.startswith(PHONE_COUNTRY_CODE_ID):
        cleaned = PHONE_LOCAL_PREFIX_ID + cleaned[3:]
    if not cleaned.isdigit():
        raise ValidationError("Nomor telepon hanya boleh berisi angka.")
    if not PHONE_MIN_LENGTH <= len(cleaned) <= PHONE_MAX_LENGTH:
        raise ValidationError("Panjang nomor telepon tidak valid.")


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
