#!/bin/bash
set -e

echo "🚀 Install deps"
pip install -r requirements.txt

echo "📦 Static"
python project/manage.py collectstatic --noinput


echo "🗄️ Migrate"
python project/manage.py migrate --noinput

echo "✅ Build done"

