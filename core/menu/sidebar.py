from django.urls import NoReverseMatch, reverse

from core.access import ALL_ROLES, DEVELOPER_ROLES, MANAGER_ROLES

PLACEHOLDER_URL = "#"

SIDEBAR_GROUPS = [
    {
        "label": "Main",
        "items": [
            {
                "label": "Dashboard",
                "icon": "fa-chart-pie",
                "url": "core:index",
                "roles": ALL_ROLES,
            },
        ],
    },
    {
        "label": "Account",
        "items": [
            {
                "label": "User",
                "icon": "fa-user-gear",
                "url": PLACEHOLDER_URL,
                "roles": MANAGER_ROLES,
            },
            {
                "label": "Profile",
                "icon": "fa-id-card",
                "url": PLACEHOLDER_URL,
                "roles": MANAGER_ROLES,
            },
        ],
    },
    {
        "label": "Core",
        "items": [
            {
                "label": "Brand",
                "icon": "fa-tags",
                "url": "core:brand-detail",
                "roles": DEVELOPER_ROLES,
            },
            {
                "label": "Orgs",
                "icon": "fa-building",
                "url": "core:orgs-detail",
                "roles": MANAGER_ROLES,
            },
        ],
    },
    {
        "label": "Preferensi",
        "items": [
            {
                "label": "Admin Panel",
                "icon": "fa-shield-halved",
                "url": PLACEHOLDER_URL,
                "roles": MANAGER_ROLES,
            },
            {
                "label": "Logout",
                "icon": "fa-arrow-right-from-bracket",
                "url": "logout",
                "roles": ALL_ROLES,
            },
        ],
    },
]


def _resolve_url(url):
    if not url or url == PLACEHOLDER_URL:
        return PLACEHOLDER_URL, None
    try:
        return reverse(url), url
    except NoReverseMatch:
        return PLACEHOLDER_URL, None


def _build_item(item, user_job):
    if user_job not in item["roles"]:
        return None
    url, url_name = _resolve_url(item["url"])
    return {
        "label": item["label"],
        "icon": item["icon"],
        "url": url,
        "url_name": url_name,
    }


def build_sidebar(user):
    if not user or not user.is_authenticated:
        return []
    user_job = getattr(user, "job", None)
    if not user_job:
        return []
    groups = []
    for group in SIDEBAR_GROUPS:
        items = []
        for item in group["items"]:
            built = _build_item(item, user_job)
            if built is not None:
                items.append(built)
        if items:
            groups.append(
                {
                    "label": group["label"],
                    "items": items,
                }
            )
    return groups
