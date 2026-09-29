from django.db.models.signals import post_save
from django.dispatch import receiver

from account.models import Profile, User


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
