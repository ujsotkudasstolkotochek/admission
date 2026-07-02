#!/bin/bash
set -e

echo "🚀 Устанавливаем зависимости..."
pip install -r requirements.txt

echo "📦 Собираем статику..."
python project/manage.py collectstatic --noinput

echo "🗄️ Пробуем применить миграции (основной путь)..."
python project/manage.py migrate --noinput || {
    echo "⚠️ Обычная миграция упала. Пробуем --fake-initial..."
    python project/manage.py migrate --fake-initial --noinput || {
        echo "⚠️ Пробуем fake для parsers..."
        python project/manage.py migrate parsers --fake || true
        python project/manage.py migrate --noinput
    }
}

echo "📋 Добавляем программы..."
python project/scripts/add_program.py

echo "🔄 Обновляем данные..."
python - << 'EOF'
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from parsers.services import update_all_programs
update_all_programs()
EOF

echo "✅ Готово!"