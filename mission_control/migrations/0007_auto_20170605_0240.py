# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-06-05 02:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mission_control', '0006_auto_20170605_0219'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='rover',
            unique_together=set([('owner', 'name')]),
        ),
    ]