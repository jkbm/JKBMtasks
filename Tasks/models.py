from django.db import models
from django.utils import timezone
from datetime import datetime
import uuid
from django.contrib.auth.models import User
from Telebot.models import Bot_user
from django.conf import settings
# Create your models here.

class Task(models.Model):
    """
    General task model
    """

    task_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, unique=False)
    description = models.CharField(max_length=200, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    finish_date = models.DateField(default=datetime.now, null=True, blank=True)
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)
    created_by_bot = models.ForeignKey(Bot_user, null=True, blank=True, on_delete=models.SET_NULL)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return "{0} | {1} [{2}]".format(self.title, self.start_date, self.completed)