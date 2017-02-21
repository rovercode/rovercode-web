from .models import Rover
from datetime import datetime, timedelta, timezone

"""
Removes from the database all rovers who haven't checked in in a certain amount of time.

:param age:
A timedelta expressing the oldest rover to keep. Any older will be removed. Must be negative.
"""
def remove_old_rovers(age):
    Rover.objects.filter(last_checkin__lte=(datetime.now(timezone.utc)+age)).delete()
