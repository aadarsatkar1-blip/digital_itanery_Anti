#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt
npm install
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --minify
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py create_superuser_if_none


