
from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.apps import apps, AppConfig
from django.conf import settings

if not settings.configured:
    # set the default Django settings module for the 'celery' program.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')  # pragma: no cover


app = Celery('rovercode_web')

class CeleryConfig(AppConfig):
    name = 'rovercode_web.taskapp'
    verbose_name = 'Celery Config'

    def ready(self):
        # Using a string here means the worker will not have to
        # pickle the object when using Windows.
        app.config_from_object('django.conf:settings')
        installed_apps = [app_config.name for app_config in apps.get_app_configs()]
        app.autodiscover_tasks(lambda: installed_apps, force=True)

        app.add_periodic_task(13.0, another_debug_task.s(), name='hi every 13')
        app.add_periodic_task(5.0, clear_old_rovers.s(), name='clear old rovers')

        if hasattr(settings, 'RAVEN_CONFIG'):
            # Celery signal registration
            from raven import Client as RavenClient
            from raven.contrib.celery import register_signal as raven_register_signal
            from raven.contrib.celery import register_logger_signal as raven_register_logger_signal

            raven_client = RavenClient(dsn=settings.RAVEN_CONFIG['DSN'])
            raven_register_logger_signal(raven_client)
            raven_register_signal(raven_client)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))  # pragma: no cover

@app.task(bind=True)
def another_debug_task(self):
    print('Hi there!!!')

@app.task(bind=True)
def clear_old_rovers(self):
    from mission_control.models import Rover
    rovers = Rover.objects.all()
    print(rovers[0].name)
