from django.core.management.base import BaseCommand

from vault.models import Storages
from vault.utils.services import recalculate_storages_occupancy


class Command(BaseCommand):
    help = "Sinkronisasi current_occupancy dan status semua gudang."

    def handle(self, *args, **options):
        storages = Storages.objects.all()
        total = storages.count()
        self.stdout.write(f"Memproses {total} gudang...")
        for s in storages:
            recalculate_storages_occupancy(s.pk)
        self.stdout.write(self.style.SUCCESS(f"Selesai. {total} gudang disinkronkan."))
