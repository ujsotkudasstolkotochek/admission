import os

_scheduler_started = False


def init_scheduler():
    global _scheduler_started

    if _scheduler_started:
        return
    _scheduler_started = True

    # защита от build/migrate фаз Render
    if os.environ.get("RUN_MAIN") == "true":
        return

    from parsers.scheduler import start_scheduler
    start_scheduler()