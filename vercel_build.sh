#!/bin/bash
python3 -m ensurepip --default-pip || curl https://bootstrap.pypa.io/get-pip.py | python3
python3 -m pip install --upgrade pip setuptools wheel

export PATH="/python312/bin:$PATH"

python3 -m pip install --no-cache-dir -r requirements.txt
echo "🔹 Checking Gunicorn installation..."
which gunicorn || echo "⚠️ Gunicorn NOT found in PATH!"
pip show gunicorn || echo "⚠️ Gunicorn NOT installed in this environment!"

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput
export PATH="$HOME/.local/bin:$PATH"

echo "🔹 Starting Gunicorn..."
gunicorn api.wsgi:application --bind 0.0.0.0:8000
