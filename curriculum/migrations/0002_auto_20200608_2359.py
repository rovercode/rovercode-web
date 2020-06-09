# Generated by Django 2.2.13 on 2020-06-08 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='goals',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='tutorial_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
