# project/parsers/management/commands/update_programs.py
from django.core.management.base import BaseCommand
from parsers.services import update_all_programs


class Command(BaseCommand):
    help = "Обновляет данные по всем программам (парсинг СПбГУ/СПбПУ/ИТМО)"

    def handle(self, *args, **options):
        update_all_programs()