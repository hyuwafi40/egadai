import importlib
from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "account"
    verbose_name = "Accounts"

    def ready(self):
        importlib.import_module("account.signals")
