import importlib

from django.apps import AppConfig


class CustomerConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "customer"
    verbose_name = "Customers"

    def ready(self):
        importlib.import_module("customer.signals")
