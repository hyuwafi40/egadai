import importlib
from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Cores"

    def ready(self):
        importlib.import_module("core.signals")
