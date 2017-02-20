from .models import Rover
from datetime import datetime, timedelta, timezone

def remove_old_rovers():
    Rover.objects.filter(last_checkin__lte=(datetime.now(timezone.utc)+timedelta(seconds=-5))).delete()
