import os
from celery import Celery
from celery.schedules import crontab
 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JKTasks.settings')
 
app = Celery('JKTasks')
app.config_from_object('django.conf:settings', namespace="CELERY")

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from JKTasks.tasks import temp_task

    # Calls print_test() every two seconds.
    sender.add_periodic_task(10.0, temp_task(), name='print test every two seconds')


app.conf.beat_schedule = {
    # Executes every Monday morning at 7:30 a.m.
    'add-every-monday-morning': {
        'task': 'JKTasks.tasks.add',
        'schedule': crontab(minute='*'),
        'args': (16, 16),
    },
}
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

