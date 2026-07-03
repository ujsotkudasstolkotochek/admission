# project/scripts/add_programs.py
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
import django
django.setup()

from parsers.models import University, Program

# ============================================================
# Университеты
# ============================================================

university_spbu, _ = University.objects.get_or_create(
    name="Санкт-Петербургский государственный университет",
    defaults={"short_name": "СПбГУ"}
)

university_spbstu, _ = University.objects.get_or_create(
    name="Санкт-Петербургский политехнический университет Петра Великого",
    defaults={"short_name": "СПбПУ"}
)

university_itmo, _ = University.objects.get_or_create(
    name="Национальный исследовательский университет ИТМО",
    defaults={"short_name": "ИТМО"}
)

university_mirea, _ = University.objects.get_or_create(
    name="МИРЭА - Российский технологический университет",
    defaults={"short_name": "МИРЭА"}
)

# ============================================================
# Список программ
# ============================================================

programs_to_add = [

    # ---------- СПбГУ ----------
    {
        "university": university_spbu,
        "code": "09.03.04",
        "name": "Программная инженерия",
        "program_name": "Программная инженерия",
        "url": "https://enrollelists.spbu.ru/reports/PriemList02.php?mode=list&education_level_sort_order=1&is_foreign=0&faculty_name=&speciality=09.03.04%7C%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BD%D0%B0%D1%8F+%D0%B8%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%B8%D1%8F&program_name=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BD%D0%B0%D1%8F+%D0%B8%D0%BD%D0%B6%D0%B5%D0%BD%D0%B5%D1%80%D0%B8%D1%8F&education_form_name=&fin_source_name=&consent_status=&contract_status=&priority=&status=&applicant_code=",
        "budget_places": 40,
    },
    {
        "university": university_spbu,
        "code": "02.03.01",
        "name": "Математика и компьютерные науки",
        "program_name": "AI360: Математика машинного обучения",
        "url": "https://enrollelists.spbu.ru/reports/PriemList02.php?mode=list&education_level_sort_order=1&is_foreign=0&faculty_name=&speciality=02.03.01%7C%D0%9C%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0+%D0%B8+%D0%BA%D0%BE%D0%BC%D0%BF%D1%8C%D1%8E%D1%82%D0%B5%D1%80%D0%BD%D1%8B%D0%B5+%D0%BD%D0%B0%D1%83%D0%BA%D0%B8&program_name=AI360%3A+%D0%9C%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0+%D0%BC%D0%B0%D1%88%D0%B8%D0%BD%D0%BD%D0%BE%D0%B3%D0%BE+%D0%BE%D0%B1%D1%83%D1%87%D0%B5%D0%BD%D0%B8%D1%8F&education_form_name=&fin_source_name=&consent_status=&contract_status=&priority=&status=&applicant_code=",
        "budget_places": 28,
    },
    {
        "university": university_spbu,
        "code": "02.03.03",
        "name": "Математическое обеспечение и администрирование информационных систем",
        "program_name": "Технологии программирования",
        "url": "https://enrollelists.spbu.ru/reports/PriemList02.php?mode=list&education_level_sort_order=1&is_foreign=0&faculty_name=&speciality=02.03.03%7C%D0%9C%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B5+%D0%BE%D0%B1%D0%B5%D1%81%D0%BF%D0%B5%D1%87%D0%B5%D0%BD%D0%B8%D0%B5+%D0%B8+%D0%B0%D0%B4%D0%BC%D0%B8%D0%BD%D0%B8%D1%81%D1%82%D1%80%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5+%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D1%85+%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC&program_name=%D0%A2%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8+%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F&education_form_name=&fin_source_name=&consent_status=&contract_status=&priority=&status=&applicant_code=",
        "budget_places": 34,
    },
    {
        "university": university_spbu,
        "code": "01.03.02",
        "name": "Прикладная математика и информатика",
        "program_name": "Прикладная математика, процессы управления и искусственный интеллект (с дополнительной квалификацией 'Программист')",
        "url": "https://enrollelists.spbu.ru/reports/PriemList02.php?mode=list&education_level_sort_order=1&is_foreign=0&faculty_name=&speciality=01.03.02%7C%D0%9F%D1%80%D0%B8%D0%BA%D0%BB%D0%B0%D0%B4%D0%BD%D0%B0%D1%8F+%D0%BC%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0+%D0%B8+%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0&program_name=%D0%9F%D1%80%D0%B8%D0%BA%D0%BB%D0%B0%D0%B4%D0%BD%D0%B0%D1%8F+%D0%BC%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0%2C+%D0%BF%D1%80%D0%BE%D1%86%D0%B5%D1%81%D1%81%D1%8B+%D1%83%D0%BF%D1%80%D0%B0%D0%B2%D0%BB%D0%B5%D0%BD%D0%B8%D1%8F+%D0%B8+%D0%B8%D1%81%D0%BA%D1%83%D1%81%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9+%D0%B8%D0%BD%D1%82%D0%B5%D0%BB%D0%BB%D0%B5%D0%BA%D1%82+%28%D1%81+%D0%B4%D0%BE%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9+%D0%BA%D0%B2%D0%B0%D0%BB%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B5%D0%B9+%22%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82%22%29&education_form_name=&fin_source_name=&consent_status=&contract_status=&priority=&status=&applicant_code=",
        "budget_places": 137,
    },
    {
        "university": university_spbu,
        "code": "01.03.02",
        "name": "Прикладная математика и информатика",
        "program_name": "Прикладная математика, современное программирование и искусственный интеллект (с дополнительной квалификацией 'Системный аналитик')",
        "url": "https://enrollelists.spbu.ru/reports/PriemList02.php?mode=list&education_level_sort_order=1&is_foreign=0&faculty_name=&speciality=01.03.02%7C%D0%9F%D1%80%D0%B8%D0%BA%D0%BB%D0%B0%D0%B4%D0%BD%D0%B0%D1%8F+%D0%BC%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0+%D0%B8+%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0&program_name=%D0%9F%D1%80%D0%B8%D0%BA%D0%BB%D0%B0%D0%B4%D0%BD%D0%B0%D1%8F+%D0%BC%D0%B0%D1%82%D0%B5%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0%2C+%D1%81%D0%BE%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D0%BE%D0%B5+%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5+%D0%B8+%D0%B8%D1%81%D0%BA%D1%83%D1%81%D1%81%D1%82%D0%B2%D0%B5%D0%BD%D0%BD%D1%8B%D0%B9+%D0%B8%D0%BD%D1%82%D0%B5%D0%BB%D0%BB%D0%B5%D0%BA%D1%82+%28%D1%81+%D0%B4%D0%BE%D0%BF%D0%BE%D0%BB%D0%BD%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%BE%D0%B9+%D0%BA%D0%B2%D0%B0%D0%BB%D0%B8%D1%84%D0%B8%D0%BA%D0%B0%D1%86%D0%B8%D0%B5%D0%B9+%22%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%BD%D1%8B%D0%B9+%D0%B0%D0%BD%D0%B0%D0%BB%D0%B8%D1%82%D0%B8%D0%BA%22%29&education_form_name=&fin_source_name=&consent_status=&contract_status=&priority=&status=&applicant_code=",
        "budget_places": 48,
    },
    {
        "university": university_spbu,
        "code": "02.03.02",
        "name": "Фундаментальная информатика и информационные технологии",
        "program_name": "Большие данные и распределенная цифровая платформа",
        "url": "https://enrollelists.spbu.ru/reports/PriemList02.php?mode=list&education_level_sort_order=1&is_foreign=0&faculty_name=&speciality=02.03.02%7C%D0%A4%D1%83%D0%BD%D0%B4%D0%B0%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0+%D0%B8+%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B5+%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8&program_name=%D0%91%D0%BE%D0%BB%D1%8C%D1%88%D0%B8%D0%B5+%D0%B4%D0%B0%D0%BD%D0%BD%D1%8B%D0%B5+%D0%B8+%D1%80%D0%B0%D1%81%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F+%D1%86%D0%B8%D1%84%D1%80%D0%BE%D0%B2%D0%B0%D1%8F+%D0%BF%D0%BB%D0%B0%D1%82%D1%84%D0%BE%D1%80%D0%BC%D0%B0&education_form_name=&fin_source_name=&consent_status=&contract_status=&priority=&status=&applicant_code=",
        "budget_places": 40,
    },
    {
        "university": university_spbu,
        "code": "02.03.02",
        "name": "Фундаментальная информатика и информационные технологии",
        "program_name": "Программирование и информационные технологии",
        "url": "https://enrollelists.spbu.ru/reports/PriemList02.php?mode=list&education_level_sort_order=1&is_foreign=0&faculty_name=&speciality=02.03.02%7C%D0%A4%D1%83%D0%BD%D0%B4%D0%B0%D0%BC%D0%B5%D0%BD%D1%82%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F+%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%82%D0%B8%D0%BA%D0%B0+%D0%B8+%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B5+%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8&program_name=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5+%D0%B8+%D0%B8%D0%BD%D1%84%D0%BE%D1%80%D0%BC%D0%B0%D1%86%D0%B8%D0%BE%D0%BD%D0%BD%D1%8B%D0%B5+%D1%82%D0%B5%D1%85%D0%BD%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8&education_form_name=&fin_source_name=&consent_status=&contract_status=&priority=&status=&applicant_code=",
        "budget_places": 40,
    },

    # ---------- СПбПУ ----------
    {
        "university": university_spbstu,
        "code": "09.03.03",
        "name": "Прикладная информатика",
        "program_name": "Прикладная информатика",
        "url": "https://my.spbstu.ru/home/abit/list-applicants/bachelor",
        "budget_places": 50,
    },
    {
        "university": university_spbstu,
        "code": "02.03.01",
        "name": "Математика и компьютерные науки",
        "program_name": "Математика и компьютерные науки",
        "url": "https://my.spbstu.ru/home/abit/list-applicants/bachelor",
        "budget_places": 41,
    },
    {
        "university": university_spbstu,
        "code": "02.03.03",
        "name": "Математическое обеспечение и администрирование информационных систем",
        "program_name": "Математическое обеспечение и администрирование информационных систем",
        "url": "https://my.spbstu.ru/home/abit/list-applicants/bachelor",
        "budget_places": 32,
    },
    {
        "university": university_spbstu,
        "code": "01.03.02",
        "name": "Прикладная математика и информатика",
        "program_name": "Прикладная математика и информатика",
        "url": "https://my.spbstu.ru/home/abit/list-applicants/bachelor",
        "budget_places": 60,
    },
    {
        "university": university_spbstu,
        "code": "09.03.01",
        "name": "Информатика и вычислительная техника",
        "program_name": "Информатика и вычислительная техника",
        "url": "https://my.spbstu.ru/home/abit/list-applicants/bachelor",
        "budget_places": 33,
    },
    {
        "university": university_spbstu,
        "code": "09.03.02",
        "name": "Информационные системы и технологии",
        "program_name": "Информационные системы и технологии",
        "url": "https://my.spbstu.ru/home/abit/list-applicants/bachelor",
        "budget_places": 31,
    },
    {
        "university": university_spbstu,
        "code": "38.03.05",
        "name": "Бизнес-информатика",
        "program_name": "Бизнес-информатика",
        "url": "https://my.spbstu.ru/home/abit/list-applicants/bachelor",
        "budget_places": 39,
    },
    {
        "university": university_spbstu,
        "code": "11.03.02",
        "name": "Инфокоммуникационные технологии и системы связи",
        "program_name": "Инфокоммуникационные технологии и системы связи",
        "url": "https://my.spbstu.ru/home/abit/list-applicants/bachelor",
        "budget_places": 62,
    },

    # ---------- ИТМО ----------
    {
        "university": university_itmo,
        "code": "2334",
        "name": "Прикладная математика и информатика",
        "program_name": "Прикладная математика и информатика",
        "url": "https://abit.itmo.ru/rating/bachelor/budget/2334",
        "budget_places": 139,
    },
    {
        "university": university_itmo,
        "code": "2335",
        "name": "Математическое обеспечение и администрирование информационных систем",
        "program_name": "Математическое обеспечение и администрирование информационных систем",
        "url": "https://abit.itmo.ru/rating/bachelor/budget/2335",
        "budget_places": 43,
    },
    {
        "university": university_itmo,
        "code": "2339",
        "name": "Информатика и вычислительная техника",
        "program_name": "Информатика и вычислительная техника",
        "url": "https://abit.itmo.ru/rating/bachelor/budget/2339",
        "budget_places": 16,
    },
    {
        "university": university_itmo,
        "code": "2340",
        "name": "Информационные системы и технологии",
        "program_name": "Информационные системы и технологии",
        "url": "https://abit.itmo.ru/rating/bachelor/budget/2340",
        "budget_places": 132,
    },
    {
        "university": university_itmo,
        "code": "2341",
        "name": "Прикладная информатика",
        "program_name": "Прикладная информатика",
        "url": "https://abit.itmo.ru/rating/bachelor/budget/2341",
        "budget_places": 24,
    },
    {
        "university": university_itmo,
        "code": "2343",
        "name": "Информационная безопасность",
        "program_name": "Информационная безопасность",
        "url": "https://abit.itmo.ru/rating/bachelor/budget/2343",
        "budget_places": 77,
    },
    {
        "university": university_itmo,
        "code": "2344",
        "name": "Инфокоммуникационные технологии и системы связи",
        "program_name": "Инфокоммуникационные технологии и системы связи",
        "url": "https://abit.itmo.ru/rating/bachelor/budget/2344",
        "budget_places": 73,
    },
    {
        "university": university_itmo,
        "code": "2356",
        "name": "Бизнес-информатика",
        "program_name": "Бизнес-информатика",
        "url": "https://abit.itmo.ru/rating/bachelor/budget/2356",
        "budget_places": 41,
    },

    # ---------- МИРЭА ----------
    {
        "university": university_mirea,
        "code": "1862638569831537974",
        "name": "Системное программирование и компьютерные технологии",
        "program_name": "Системное программирование и компьютерные технологии",
        "url": "https://priem.mirea.ru/accepted-entrants-list/competition?comp_ids=1862638569831537974&edu_level=2&org_unit_id=14840287700495285107&edu_form_id=1",
        "budget_places": 19,
    },

    {
        "university": university_mirea,
        "code": "1862532990899330358",
        "name": "Анализ данных",
        "program_name": "Анализ данных",
        "url": "https://priem.mirea.ru/accepted-entrants-list/competition?comp_ids=1862532990899330358&edu_level=2&org_unit_id=1484028700495285107&edu_form_id=1",
        "budget_places": 21,
    },

    {
        "university": university_mirea,
        "code": "1862638576237288758",
        "name": "Бизнес-аналитика",
        "program_name": "Бизнес-аналитика",
        "url": "https://priem.mirea.ru/accepted-entrants-list/competition?comp_ids=1862638576237288758&edu_level=2&org_unit_id=1484028700495285107&edu_form_id=1",
        "budget_places": 18,
    },

    {
        "university": university_mirea,
        "code": "1862638630198058294",
        "name": "Инфраструктура информационных технологий",
        "program_name": "Инфраструктура информационных технологий",
        "url": "https://priem.mirea.ru/accepted-entrants-list/competition?comp_ids=1862638630198058294&edu_level=2&org_unit_id=1484028700495285107&edu_form_id=1",
        "budget_places": 27,
    },

    {
        "university": university_mirea,
        "code": "1862533213266648374",
        "name": "Технологии разработки платформенных бизнес-приложений",
        "program_name": "Технологии разработки платформенных бизнес-приложений",
        "url": "https://priem.mirea.ru/accepted-entrants-list/competition?comp_ids=1862533213266648374&edu_level=2&org_unit_id=1484028700495285107&edu_form_id=1",
        "budget_places": 40,
    },

    {
        "university": university_mirea,
        "code": "1862638696623250742",
        "name": "Разработка кроссплатформенных бизнес-приложений",
        "program_name": "Разработка кроссплатформенных бизнес-приложений",
        "url": "https://priem.mirea.ru/accepted-entrants-list/competition?comp_ids=1862638696623250742&edu_level=2&org_unit_id=1484028700495285107&edu_form_id=1",
        "budget_places": 46,
    },

    {
        "university": university_mirea,
        "code": "1862638703059410230",
        "name": "Технологии искусственного интеллекта и анализ данных",
        "program_name": "Технологии искусственного интеллекта и анализ данных",
        "url": "https://priem.mirea.ru/accepted-entrants-list/competition?comp_ids=1862638703059410230&edu_level=2&org_unit_id=1484028700495285107&edu_form_id=1",
        "budget_places": 50,
    },

    {
        "university": university_mirea,
        "code": "1862638710286196022",
        "name": "Технологии разработки программного обеспечения полного цикла",
        "program_name": "Технологии разработки программного обеспечения полного цикла",
        "url": "https://priem.mirea.ru/accepted-entrants-list/competition?comp_ids=1862638710286196022&edu_level=2&org_unit_id=1484028700495285107&edu_form_id=1",
        "budget_places": 33,
    },

    {
        "university": university_mirea,
        "code": "1862638731367816502",
        "name": "Управление данными",
        "program_name": "Управление данными",
        "url": "https://priem.mirea.ru/accepted-entrants-list/competition?comp_ids=1862638731367816502&edu_level=2&org_unit_id=1484028700495285107&edu_form_id=1",
        "budget_places": 28,
    },

    {
        "university": university_mirea,
        "code": "1862638745412443446",
        "name": "Интеллектуальные системы поддержки принятия решений",
        "program_name": "Интеллектуальные системы поддержки принятия решений",
        "url": "https://priem.mirea.ru/accepted-entrants-list/competition?comp_ids=1862638745412443446&edu_level=2&org_unit_id=1484028700495285107&edu_form_id=1",
        "budget_places": 25,
    },

    {
        "university": university_mirea,
        "code": "1862638830212881718",
        "name": "Аудиовизуальные системы и технологии медиасвязи",
        "program_name": "Аудиовизуальные системы и технологии медиасвязи",
        "url": "https://priem.mirea.ru/accepted-entrants-list/competition?comp_ids=1862638830212881718&edu_level=2&org_unit_id=1484028700495285107&edu_form_id=1",
        "budget_places": 33,
    },

    {
        "university": university_mirea,
        "code": "1862638837220515126",
        "name": "Инфокоммуникационные системы и сети",
        "program_name": "Инфокоммуникационные системы и сети",
        "url": "https://priem.mirea.ru/accepted-entrants-list/competition?comp_ids=1862638837220515126&edu_level=2&org_unit_id=1484028700495285107&edu_form_id=1",
        "budget_places": 48,
    },

]

# ============================================================
# Загрузка программ в БД
# ============================================================

def safe(v, limit=5000):
    if not v:
        return ""
    return str(v)[:limit]

added = 0
updated = 0
unchanged = 0

for prog_data in programs_to_add:
    obj, created = Program.objects.get_or_create(
        university=prog_data["university"],
        code=prog_data["code"],
        name=safe(prog_data["name"]),
        defaults={
            "program_name": safe(prog_data["program_name"]),
            "url": prog_data["url"],
            "budget_places": prog_data["budget_places"],
        }
    )
    if created:
        print(f"✅ Добавлена программа: {prog_data['code']} - {prog_data['name']}")
        added += 1
    else:
        # Проверяем, изменились ли данные
        changed = False
        if obj.program_name != prog_data["program_name"]:
            obj.program_name = prog_data["program_name"]
            changed = True
        if obj.url != prog_data["url"]:
            obj.url = prog_data["url"]
            changed = True
        if obj.budget_places != prog_data["budget_places"]:
            obj.budget_places = prog_data["budget_places"]
            changed = True
        if changed:
            obj.save()
            print(f"🔄 Обновлена программа: {prog_data['code']} - {prog_data['name']}")
            updated += 1
        else:
            print(f"⏩ Без изменений: {prog_data['code']} - {prog_data['name']}")
            unchanged += 1

print("=" * 60)
print(f"Итог: добавлено {added}, обновлено {updated}, без изменений {unchanged}.")