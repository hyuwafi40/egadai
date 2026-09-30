import importlib

from django.apps import AppConfig


class VaultConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "vault"
    verbose_name = "Vaults"

    def ready(self):
        importlib.import_module("vault.signals")
