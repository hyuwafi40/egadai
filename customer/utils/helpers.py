def normalize_text(value):
    if not value:
        return value
    return value.strip()


def normalize_nik(value):
    if not value:
        return value
    cleaned = value.strip()
    cleaned = cleaned.replace(" ", "").replace("-", "")
    return cleaned


def normalize_code(value):
    if not value:
        return value
    return value.strip().upper()
