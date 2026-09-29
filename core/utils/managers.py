from django.core.cache import cache
from django.db import models

from core.utils.helpers import singleton_cache_key


class SingletonManager(models.Manager):
    def get_current(self):
        key = singleton_cache_key(self.model._meta.model_name)
        instance = cache.get(key)
        if instance is not None:
            return instance
        instance = self.filter(pk=1).first()
        if instance is not None:
            cache.set(key, instance, timeout=None)
        return instance
