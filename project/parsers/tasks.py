from celery import shared_task
from .services import update_all_programs

@shared_task
def update_statistics():
    update_all_programs()