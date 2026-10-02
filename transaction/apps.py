import importlib

from django.apps import AppConfig


class TransactionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "transaction"
    verbose_name = "Transactions"

    def ready(self):
        importlib.import_module("transaction.signals")
