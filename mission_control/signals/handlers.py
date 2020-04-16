"""Mission Control signal handlers."""
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.template import loader

import requests

from mission_control.models import BlockDiagram

LOGGER = logging.getLogger(__name__)


@receiver(pre_save, sender=BlockDiagram, dispatch_uid="update_block_diagram")
def update_block_diagram(sender, instance, **kwargs):
    """Handle changes to BlockDiagram model."""
    response = requests.post(
        '{}/censor-word/{}'.format(settings.PROFANITY_CHECK_SERVICE_HOST, instance.name))

    if response.status_code != 200:
        LOGGER.error(
            'Error %s contacting profanity check', response.status_code)
        return

    profane_word = response.json()['original_profane_word']
    if profane_word and not instance.flagged:
        instance.flagged = True

        body = loader.render_to_string('email/profanity_notification.html', {
            'user': instance.user,
            'name': instance.name,
            'word': profane_word,
        })
        send_mail(
            'Profanity Detected',
            body,
            settings.DEFAULT_FROM_EMAIL,
            ['conduct@rovercode.com']
        )
    elif not profane_word and instance.flagged:
        instance.flagged = False
