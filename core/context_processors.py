from django.db import DatabaseError

from core.utils.services import get_brand, get_orgs


def brand_orgs(request):
    try:
        return {
            "brand": get_brand(),
            "orgs": get_orgs(),
        }
    except DatabaseError:
        return {
            "brand": None,
            "orgs": None,
        }
