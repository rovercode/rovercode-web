# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-01-29 05:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission_control', '0010_add_i2c_eyes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rover',
            name='local_ip',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
