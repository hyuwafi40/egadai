from django.core.cache import cache
from django.urls import NoReverseMatch, reverse

from core.access import ALL_ROLES, DEVELOPER_ROLES, MANAGER_ROLES

PLACEHOLDER_URL = "#"
REVERSE_CACHE = {}
SIDEBAR_CACHE_KEY = "core.sidebar.{job}"

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
            {
                "label": "Transaksi Baru",
                "icon": "fa-plus-circle",
                "url": "transaction:new",
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
                "url": "account:user-list",
                "roles": MANAGER_ROLES,
            },
            {
                "label": "Profile",
                "icon": "fa-id-card",
                "url": "account:profile-detail",
                "roles": ALL_ROLES,
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
        "label": "Vault",
        "items": [
            {
                "label": "Category",
                "icon": "fa-layer-group",
                "url": "vault:category-list",
                "roles": MANAGER_ROLES,
            },
            {
                "label": "Scheme",
                "icon": "fa-file-contract",
                "url": "vault:scheme-list",
                "roles": MANAGER_ROLES,
            },
            {
                "label": "Storages",
                "icon": "fa-warehouse",
                "url": "vault:storages-list",
                "roles": MANAGER_ROLES,
            },
        ],
    },
    {
        "label": "Customer",
        "items": [
            {
                "label": "Nasabah",
                "icon": "fa-users",
                "url": "customer:list",
                "roles": ALL_ROLES,
            },
        ],
    },
    {
        "label": "Collateral",
        "items": [
            {
                "label": "Barang Jaminan",
                "icon": "fa-boxes-stacked",
                "url": "collateral:list",
                "roles": ALL_ROLES,
            },
        ],
    },
    {
        "label": "Transaction",
        "items": [
            {
                "label": "Transaksi Gadai",
                "icon": "fa-hand-holding-dollar",
                "url": "transaction:list",
                "roles": ALL_ROLES,
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
    if url in REVERSE_CACHE:
        return REVERSE_CACHE[url]
    try:
        resolved = reverse(url)
        pair = (resolved, url)
    except NoReverseMatch:
        pair = (PLACEHOLDER_URL, None)
    REVERSE_CACHE[url] = pair
    return pair


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


def _build_groups(user_job):
    groups = []
    for group in SIDEBAR_GROUPS:
        items = []
        for item in group["items"]:
            built = _build_item(item, user_job)
            if built is not None:
                items.append(built)
        if items:
            groups.append({"label": group["label"], "items": items})
    return groups


def build_sidebar(user):
    if not user or not user.is_authenticated:
        return []
    user_job = getattr(user, "job", None)
    if not user_job:
        return []
    cache_key = SIDEBAR_CACHE_KEY.format(job=user_job)
    cached = cache.get(cache_key)
    if cached is not None:
        return cached
    groups = _build_groups(user_job)
    cache.set(cache_key, groups, timeout=None)
    return groups
