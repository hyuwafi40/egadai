def normalize_text(value):
    if not value:
        return value
    return value.strip()


def normalize_code(value):
    if not value:
        return value
    return value.strip().upper()
