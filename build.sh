#!/bin/bash
set -e

echo "🚀 Устанавливаем зависимости..."
pip install -r requirements.txt

echo "📦 Собираем статику..."
python manage.py collectstatic --noinput

echo "🗄️ Применяем миграции..."
python manage.py migrate

echo "✅ Сборка завершена!"