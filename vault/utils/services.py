from django.db import transaction as db_transaction

from vault.models import Storages
from vault.utils.constants import StorageStatusChoices


def recalculate_storages_occupancy(storages_id):
    if not storages_id:
        return
    from collateral.models import Collateral
    from collateral.utils.constants import CollateralStatusChoices

    with db_transaction.atomic():
        storages = Storages.objects.select_for_update().filter(pk=storages_id).first()
        if not storages:
            return
        occupancy = Collateral.objects.filter(
            storages_id=storages_id,
            is_active=True,
            status=CollateralStatusChoices.STORED,
        ).count()
        storages.current_occupancy = occupancy
        if storages.status != StorageStatusChoices.RUSAK:
            if storages.capacity and occupancy >= storages.capacity:
                storages.status = StorageStatusChoices.PENUH
            else:
                storages.status = StorageStatusChoices.TERSEDIA
        storages.save(
            update_fields=[
                "current_occupancy",
                "status",
                "updated_at",
            ]
        )
