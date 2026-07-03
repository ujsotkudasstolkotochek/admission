#!/bin/bash
set -e

echo "🚀 Install deps"
pip install -r requirements.txt

echo "🗄️ Migrate"
python project/manage.py migrate --noinput

echo "📦 Static"
python project/manage.py collectstatic --noinput

echo "📥 Add programs"
python project/scripts/add_program.py

echo "✅ Build done"
