from django.db import models

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