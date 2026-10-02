from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from collateral.models import Collateral
from vault.utils.services import recalculate_storages_occupancy


@receiver(pre_save, sender=Collateral)
def collateral_pre_save(sender, instance, **kwargs):
    if instance.pk:
        old = (
            Collateral.objects.filter(pk=instance.pk)
            .values_list("storages_id", flat=True)
            .first()
        )
        instance._old_storages_id = old
    else:
        instance._old_storages_id = None


@receiver(post_save, sender=Collateral)
def collateral_post_save(sender, instance, **kwargs):
    current = instance.storages_id
    old = getattr(instance, "_old_storages_id", None)
    recalculate_storages_occupancy(current)
    if old and old != current:
        recalculate_storages_occupancy(old)


@receiver(post_delete, sender=Collateral)
def collateral_post_delete(sender, instance, **kwargs):
    if instance.storages_id:
        recalculate_storages_occupancy(instance.storages_id)
