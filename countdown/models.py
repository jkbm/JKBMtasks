from django.db import models
from django.utils import timezone
from datetime import datetime, timedelta
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Countdown(models.Model):
    """
    General countdown model
    """

    countdown_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    countdown_to = models.DateTimeField()
    created_by = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.SET_NULL)\
    
    def __str__(self):
        return self.title