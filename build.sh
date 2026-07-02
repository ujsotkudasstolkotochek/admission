#!/bin/bash
set -e  # останавливаемся при любой ошибке

echo "🚀 Устанавливаем зависимости..."
pip install -r requirements.txt

echo "📦 Собираем статику..."
python project/manage.py collectstatic --noinput

echo "🗄️ Применяем миграции (создаём, если нужно)..."
python project/manage.py makemigrations
python project/manage.py migrate   # теперь только один раз

echo "📋 Загружаем / обновляем программы..."
python project/manage.py add_programs
python project/manage.py update_all_programs

echo "✅ Сборка завершена!"