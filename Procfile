web: gunicorn api.wsgi
worker: celery -A notifications --loglevel=INFO --broker=$REDISCLOUD_URL
