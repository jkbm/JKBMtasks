from django.db import models
from datetime import datetime
import uuid

# Create your models here.

class Bot_user(models.Model):

    id = models.CharField(primary_key=True, max_length=100, null=False, blank=False)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True,  blank=True)
    username = models.CharField(max_length=150, null=True,  blank=True)
    daily_tasks = models.BooleanField(default=False)
    app_user = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):

        return self.id + " " + str(self.username)

class Message(models.Model):

    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    chat_id = models.CharField(max_length=50)
    text = models.TextField()
    time_sent = models.DateTimeField()
    sent = models.BooleanField(default=False)
