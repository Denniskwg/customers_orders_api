#!/bin/bash

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn customers_orders_api.wsgi:application
