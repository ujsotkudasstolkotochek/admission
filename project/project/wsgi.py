import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

application = get_wsgi_application()

# ⚠️ запуск ТОЛЬКО после инициализации Django
from project.startup import init_scheduler
init_scheduler()