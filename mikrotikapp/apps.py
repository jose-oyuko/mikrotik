from django.apps import AppConfig
from .utils import setup_logging


class MikrotikappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mikrotikapp"

    def ready(self):
        """
        Initialize logging when Django starts
        """
        setup_logging()
