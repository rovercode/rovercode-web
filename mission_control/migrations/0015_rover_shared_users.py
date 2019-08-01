# Generated by Django 2.2.3 on 2019-08-01 01:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mission_control', '0014_auto_20190624_0247'),
    ]

    operations = [
        migrations.AddField(
            model_name='rover',
            name='shared_users',
            field=models.ManyToManyField(blank=True, related_name='shared_rovers', to=settings.AUTH_USER_MODEL),
        ),
    ]
