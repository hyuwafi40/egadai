from django.core.cache import cache

from account.models import Profile
from account.utils.helpers import profile_cache_key


def get_profile(user):
    key = profile_cache_key(user.pk)
    profile = cache.get(key)
    if profile is None:
        profile, _ = Profile.objects.get_or_create(user=user)
        cache.set(key, profile, timeout=None)
    return profile
