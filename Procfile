web: gunicorn api.wsgi
worker: celery -A notifications --broker=$REDISCLOUD_URL
