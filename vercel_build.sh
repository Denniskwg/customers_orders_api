#!/bin/bash

python3 -m pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py collectstatic --noinput
gunicorn api.wsgi:application --bind 0.0.0.0:8000
