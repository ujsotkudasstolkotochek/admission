# parsers/scheduler.py
import os
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .services import update_all_programs

# Флаг для включения/отключения планировщика (можно через переменную окружения)
SCHEDULER_ENABLED = os.environ.get('SCHEDULER_ENABLED', 'True') == 'True'


def start_scheduler():
    if not SCHEDULER_ENABLED:
        print("⏹ Планировщик отключён через переменную окружения")
        return

    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), 'default')

    # Добавляем задачу
    scheduler.add_job(
        update_all_programs,
        'interval',
        minutes=10,  # можно вынести в переменную окружения
        id='update_stats',
        replace_existing=True,
    )
    scheduler.start()
    print("✅ Планировщик APScheduler запущен (задача каждые 10 минут)")