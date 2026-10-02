import importlib

from django.apps import AppConfig


class CollateralConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "collateral"
    verbose_name = "Collaterals"

    def ready(self):
        importlib.import_module("collateral.signals")
