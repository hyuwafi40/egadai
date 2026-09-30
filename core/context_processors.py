from django.db import DatabaseError

from core.menu import build_footer, build_navbar, build_sidebar
from core.utils.constants import FALLBACK_APP_NAME
from core.utils.services import get_brand, get_orgs


def brand_orgs(request):
    try:
        return {
            "brand": get_brand(),
            "orgs": get_orgs(),
            "fallback_app_name": FALLBACK_APP_NAME,
        }
    except DatabaseError:
        return {
            "brand": None,
            "orgs": None,
            "fallback_app_name": FALLBACK_APP_NAME,
        }


def menus(request):
    user = getattr(request, "user", None)
    return {
        "sidebar_items": build_sidebar(user),
        "navbar_data": build_navbar(user),
        "footer_data": build_footer(),
    }
