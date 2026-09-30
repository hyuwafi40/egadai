from django.utils import timezone


def build_footer():
    return {
        "year": timezone.now().year,
    }
