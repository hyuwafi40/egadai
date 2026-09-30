from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from account.models import User
from account.models.profile import Profile
from account.utils.helpers import profile_cache_key


@receiver(post_save, sender=User)
def create_profile_on_user_create(
    sender,
    instance,
    created,
    raw=False,
    **kwargs,
):
    if raw:
        return
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=Profile)
@receiver(post_delete, sender=Profile)
def invalidate_profile_cache(sender, instance, **kwargs):
    cache.delete(profile_cache_key(instance.user_id))
