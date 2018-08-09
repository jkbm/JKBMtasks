# Generated by Django 2.0.7 on 2018-08-03 15:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Telebot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bot_user',
            name='app_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bot_user',
            name='first_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]