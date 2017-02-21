from test_plus.test import TestCase

from django.core.urlresolvers import reverse

from mission_control.models import Rover
from mission_control.utils import remove_old_rovers

import time
from datetime import timedelta

class TestRemoveOldRovers(TestCase):

    def test_rover(self):
        Rover.objects.create(
            name='rover',
            owner='jimbo',
            local_ip='8.8.8.8'
        )
        self.assertEqual(1, Rover.objects.count())
        time.sleep(1)
        Rover.objects.create(
            name='rover2',
            owner='jimbo',
            local_ip='8.8.8.8'
        )
        remove_old_rovers(timedelta(seconds=-1));
        self.assertEqual(1, Rover.objects.count())
