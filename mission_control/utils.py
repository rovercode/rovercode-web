from .models import Rover
from datetime import datetime, timedelta, timezone

"""
Removes from the database all rovers who haven't checked in in the last 5 seconds.
"""
def remove_old_rovers():
    Rover.objects.filter(last_checkin__lte=(datetime.now(timezone.utc)+timedelta(seconds=-5))).delete()
