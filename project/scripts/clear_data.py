import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from parsers.models import Applicant, Program, University

print("🧹 Очистка базы данных...")

# Удаляем в правильном порядке (сначала дочерние, потом родительские)
applicants_deleted = Applicant.objects.all().delete()
programs_deleted = Program.objects.all().delete()
universities_deleted = University.objects.all().delete()

print(f"✅ Удалено абитуриентов: {applicants_deleted[0]}")
print(f"✅ Удалено программ: {programs_deleted[0]}")
print(f"✅ Удалено университетов: {universities_deleted[0]}")
print("✅ База данных очищена.")