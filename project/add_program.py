import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from parsers.models import University, Program

# Создаём университет (если его нет)
uni, _ = University.objects.get_or_create(
    name="Санкт-Петербургский государственный университет",
    defaults={"short_name": "СПбГУ"}
)

# Создаём программу (если её нет)
Program.objects.get_or_create(
    university=uni,
    code="09.03.03",
    name="Прикладная информатика",
    defaults={
        "program_name": "Искусственный интеллект и наука о данных",
        "url": "https://enrollelists.spbu.ru/reports/PriemList02.php?mode=list&education_level_sort_order=1&speciality=09.03.03%7C%D0%9F%D1%80%D0%B8%D0%BA%D0%BB%D0%B0%D0%B4%D0%BD%D0%B0%D1%8F+%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0&program_name=%D0%98%D1%81%D0%BA%D1%83%D1%81%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9+%D0%B8%D0%BD%D1%82%D0%B5%D0%BB%D0%BB%D0%B5%D0%BA%D1%82+%D0%B8+%D0%BD%D0%B0%D1%83%D0%BA%D0%B0+%D0%BE+%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D1%85&education_form_name=&fin_source_name=&faculty_name=&is_foreign=0",
        "budget_places": 51,
    }
)

print("✅ Программа добавлена (или уже существовала)")