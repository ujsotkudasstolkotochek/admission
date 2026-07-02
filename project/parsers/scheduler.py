import os
import fcntl
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .services import update_all_programs

scheduler = BackgroundScheduler()

LOCK_FILE = "/tmp/apscheduler.lock"
lock_handle = None

_scheduler_started = False


def acquire_lock():
    global lock_handle

    lock_handle = open(LOCK_FILE, "w")

    try:
        fcntl.flock(lock_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return True
    except Exception:
        return False


def job():
    try:
        update_all_programs()
        print("✅ Programs updated")
    except Exception as e:
        print("❌ Scheduler error:", e)


def start_scheduler():
    global _scheduler_started

    if _scheduler_started:
        return
    _scheduler_started = True

    if not acquire_lock():
        print("⏹ Scheduler already running in another process")
        return

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
    print("🚀 APScheduler started (single instance)")