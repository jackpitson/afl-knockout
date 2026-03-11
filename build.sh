#!/usr/bin/env bash
set -e

python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install gunicorn

python manage.py migrate
python manage.py collectstatic --noinput

pip install -r requirements.txt

python manage.py migrate

echo "from django.contrib.auth import get_user_model;
User = get_user_model();
User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin','admin@example.com','admin123')" | python manage.py shell