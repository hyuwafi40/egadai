from django.apps import apps
from django.core.cache import cache
from django.db.models.signals import post_delete, post_migrate, post_save
from django.dispatch import receiver

from core.models import Brand, Orgs
from core.utils.helpers import singleton_cache_key


@receiver(post_migrate)
def bootstrap_singletons(sender, **kwargs):
    label = getattr(sender, "label", None)
    if label != "core":
        return
    brand_model = apps.get_model("core", "Brand")
    orgs_model = apps.get_model("core", "Orgs")
    brand_model.objects.get_or_create(pk=1)
    orgs_model.objects.get_or_create(pk=1)


@receiver(post_save, sender=Brand)
@receiver(post_save, sender=Orgs)
@receiver(post_delete, sender=Brand)
@receiver(post_delete, sender=Orgs)
def invalidate_singleton_cache(sender, instance, **kwargs):
    model_name = sender._meta.model_name
    cache.delete(singleton_cache_key(model_name))
