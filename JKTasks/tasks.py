import logging
from JKTasks.celery import app
from datetime import datetime
import time

logger = logging.getLogger('django')
@app.task(name='minute')
def temp_task():
    print("HEEEEEEEEEEEEEEEEEEEEEy")
    logger.info("Temp task executed!")

@app.task()
def add(x, y):
    time = datetime.now()
    print(str(x+y))
    print(time)

    return time.strftime('%X %x %Z')