from core.utils.constants import (
    SINGLETON_CACHE_PREFIX,
    SINGLETON_CACHE_SUFFIX,
)


def normalize_url(url):
    if not url:
        return url
    return url.strip()


def normalize_text(value):
    if not value:
        return value
    return value.strip()


def singleton_cache_key(model_name):
    return f"{SINGLETON_CACHE_PREFIX}." f"{model_name}." f"{SINGLETON_CACHE_SUFFIX}"
