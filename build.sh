#!/bin/bash
set -e  # остановка при любой ошибке

echo "🚀 Устанавливаем зависимости..."
pip install -r requirements.txt

echo "📦 Собираем статику..."
python project/manage.py collectstatic --noinput

echo "🗄️ Применяем миграции (создаём, если нужно)..."
python project/manage.py makemigrations
python project/manage.py migrate

echo "📋 Добавляем программы из скрипта..."
python project/scripts/add_program.py   # ← исправленный путь

echo "🔄 Обновляем все программы через сервис..."
python -c "
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()
from project.parsers.services import update_all_programs   # ← исправленный импорт
update_all_programs()
"

echo "✅ Сборка завершена!"