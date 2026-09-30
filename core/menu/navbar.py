from django.core.exceptions import ObjectDoesNotExist


def _get_avatar_url(user):
    try:
        profile = user.profile
    except ObjectDoesNotExist:
        return None
    if not profile:
        return None
    if not profile.photo:
        return None
    try:
        return profile.photo.url
    except ValueError:
        return None


def build_navbar(user):
    if not user or not user.is_authenticated:
        return {}
    display_name = user.get_full_name() or user.username
    role_label = user.get_job_display() if hasattr(user, "get_job_display") else ""
    initial = display_name[:1].upper() if display_name else "?"
    return {
        "display_name": display_name,
        "role_label": role_label,
        "avatar_url": _get_avatar_url(user),
        "initial": initial,
        "username": user.username,
        "email": user.email,
    }
