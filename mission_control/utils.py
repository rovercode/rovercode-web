"""Mission Control utils."""
from datetime import datetime, timezone

from .models import Rover


def remove_old_rovers(age):
    """
    Remove inactive rovers from the database.

    Rovers are determined to be inactive when they haven't checked in a certain
    amount of time.

    :param age:
        A timedelta expressing the oldest rover to keep. Any older will be
        removed. Must be negative.
    """
    Rover.objects.filter(
        last_checkin__lte=(datetime.now(timezone.utc) + age)).delete()
