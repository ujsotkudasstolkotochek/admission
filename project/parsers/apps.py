from django.apps import AppConfig

class ParsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "parsers"

    def ready(self):
        import os

        if os.environ.get("RUN_MAIN") == "true":
            return  # защита от dev reload

        from .scheduler import start_scheduler
        start_scheduler()