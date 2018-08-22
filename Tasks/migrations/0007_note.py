# Generated by Django 2.0.7 on 2018-08-22 17:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Telebot', '0005_message'),
        ('Tasks', '0006_task_created_by_bot'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('note_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, default=' ', max_length=200, null=True)),
                ('description', models.TextField(blank=True, max_length=600, null=True)),
                ('created_date', models.DateField(blank=True, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('created_by_bot', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Telebot.Bot_user')),
            ],
        ),
    ]
