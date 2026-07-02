# parsers/apps.py
from django.apps import AppConfig
import os

class ParsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'parsers'

    def ready(self):
        USE_CELERY = os.environ.get('USE_CELERY', 'False') == 'True'
        if not USE_CELERY:
            print(1)
            from .scheduler import start_scheduler
            start_scheduler()
        else:
            print("⏩ Используется Celery, планировщик APScheduler не запущен")