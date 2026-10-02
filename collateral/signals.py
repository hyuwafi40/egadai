from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from collateral.models import Collateral
from vault.utils.services import recalculate_storages_occupancy


@receiver(pre_save, sender=Collateral)
def collateral_pre_save(sender, instance, **kwargs):
    if instance.pk:
        old = (
            Collateral.objects.filter(pk=instance.pk)
            .values("storages_id", "status", "is_active")
            .first()
        )
        if old:
            instance._old_storages_id = old["storages_id"]
            instance._old_status = old["status"]
            instance._old_is_active = old["is_active"]
        else:
            instance._old_storages_id = None
            instance._old_status = None
            instance._old_is_active = None
    else:
        instance._old_storages_id = None
        instance._old_status = None
        instance._old_is_active = None


@receiver(post_save, sender=Collateral)
def collateral_post_save(sender, instance, **kwargs):
    current_storages = instance.storages_id
    current_status = instance.status
    current_is_active = instance.is_active
    old_storages = getattr(instance, "_old_storages_id", None)
    old_status = getattr(instance, "_old_status", None)
    old_is_active = getattr(instance, "_old_is_active", None)
    storages_changed = old_storages != current_storages
    status_changed = old_status != current_status
    is_active_changed = old_is_active != current_is_active
    if not storages_changed and not status_changed and not is_active_changed:
        return
    recalculate_storages_occupancy(current_storages)
    if old_storages and storages_changed:
        recalculate_storages_occupancy(old_storages)


@receiver(post_delete, sender=Collateral)
def collateral_post_delete(sender, instance, **kwargs):
    if instance.storages_id:
        recalculate_storages_occupancy(instance.storages_id)
