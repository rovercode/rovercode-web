from test_plus.test import TestCase

from django.core.urlresolvers import reverse

from mission_control.models import Rover
from mission_control.utils import remove_old_rovers

import time

class TestRemoveOldRovers(TestCase):

    def test_rover(self):
        Rover.objects.create(
            name='rover',
            owner='jimbo',
            local_ip='8.8.8.8'
        )
        rovers = Rover.objects.all()
        self.assertEqual(1, len(rovers))
        time.sleep(6)
        remove_old_rovers();
        rovers = Rover.objects.all()
        self.assertEqual(0, len(rovers))
