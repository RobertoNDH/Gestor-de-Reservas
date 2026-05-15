#!/usr/bin/env bash
# exit on error
set -o errexit

python -m pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Crea un superusuario automáticamente usando las variables de entorno de Render
python manage.py createsuperuser --noinput --username admin --email admin@reservatech.com || true
