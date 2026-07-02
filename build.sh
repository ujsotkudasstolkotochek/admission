#!/bin/bash
set -e

echo "🚀 Устанавливаем зависимости..."
pip install -r requirements.txt

echo "📦 Собираем статику..."
python project/manage.py collectstatic --noinput

echo "🗄️ Пробуем применить миграции (основной путь)..."
python manage.py migrate --fake-initial || true
python manage.py migrate --fake parsers || true
python manage.py migrate

echo "🧠 Проверяем/создаём новые миграции (безопасно)..."
python project/manage.py makemigrations --noinput || true

echo "📋 Добавляем программы из скрипта..."
python project/scripts/add_program.py

echo "🔄 Обновляем все программы через сервис..."
python - << 'EOF'
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from parsers.services import update_all_programs
update_all_programs()
EOF

echo "✅ Сборка завершена!"