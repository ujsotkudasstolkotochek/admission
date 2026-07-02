# parsers/scheduler.py
import os
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .services import update_all_programs
from django.db import connection
from django.db.utils import OperationalError

SCHEDULER_ENABLED = os.environ.get('SCHEDULER_ENABLED', 'True') == 'True'

def start_scheduler():
    if not SCHEDULER_ENABLED:
        print("⏹ Планировщик отключён через переменную окружения")
        return

    # Проверяем, существует ли таблица для хранения задач
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM django_apscheduler_djangojob LIMIT 1")
    except OperationalError:
        print("⚠️ Таблица django_apscheduler_djangojob не существует. Планировщик не запущен. Выполните миграции и запустите вручную.")
        return

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')
    scheduler.add_job(
        update_all_programs,
        'interval',
        minutes=10,
        id='update_stats',
        replace_existing=True,
    )
    scheduler.start()
    print("✅ Планировщик APScheduler запущен (задача каждые 10 минут)")
