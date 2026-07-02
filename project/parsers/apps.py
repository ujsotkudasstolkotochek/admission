from django.apps import AppConfig
import os

class ParsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "parsers"

    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()