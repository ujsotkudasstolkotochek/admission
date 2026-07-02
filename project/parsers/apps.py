from django.apps import AppConfig
import os

class ParsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "parsers"

    def ready(self):
        # защита от двойного запуска Django
        if os.environ.get("RUN_MAIN") != "true":
            return

        from .scheduler import start_scheduler
        start_scheduler()