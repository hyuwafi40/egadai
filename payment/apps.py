import importlib

from django.apps import AppConfig


class PaymentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "payment"
    verbose_name = "Payments"

    def ready(self):
        importlib.import_module("payment.signals")
