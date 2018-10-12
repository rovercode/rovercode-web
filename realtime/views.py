"""Views for the Realtime app."""
import json
from django.shortcuts import render
from django.utils.safestring import mark_safe


def index(request):
    """Return the landing page for Realtime debugging."""
    return render(request, 'realtime/index.html', {})


def room(request, room_name):
    """Return the a room page Realtime debugging."""
    return render(request, 'realtime/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
