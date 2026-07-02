from django.apps import AppConfig
from django.db.models.signals import post_migrate

class ParsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'parsers'

    def ready(self):
        from .scheduler import start_scheduler
        # Запускаем планировщик после завершения всех миграций
        post_migrate.connect(start_scheduler, sender=self)
