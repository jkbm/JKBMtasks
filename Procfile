web: gunicorn JKTasks.wsgi --log-file -
worker: celery -A JKTasks worker
beat: celery -A JKTasks beat -S django