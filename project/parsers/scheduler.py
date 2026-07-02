import os
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .services import update_all_programs

scheduler = BackgroundScheduler()

def job():
    try:
        update_all_programs()
        print("✅ Programs updated")
    except Exception as e:
        print("❌ Scheduler error:", e)


def start_scheduler():
    if os.environ.get("SCHEDULER_ENABLED", "true").lower() != "true":
        print("⏹ Scheduler disabled")
        return

    # защита от повторного старта
    if scheduler.running:
        return

    scheduler.add_jobstore(DjangoJobStore(), "default")

    scheduler.add_job(
        job,
        trigger="interval",
        minutes=10,
        id="update_programs_job",
        replace_existing=True,
        max_instances=1,
        coalesce=True,
    )

    scheduler.start()
    print("🚀 APScheduler started")