# Generated by Django 2.2 on 2019-04-17 15:58

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mission_control', '0012_auto_20190217_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rover',
            name='config',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict),
        ),
    ]