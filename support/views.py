"""Views for the Support app."""
import json
from django.shortcuts import render
from django.utils.safestring import mark_safe


def index(request):
    """Return the landing page for Support debugging."""
    return render(request, 'support/index.html', {})


def room(request, room_name):
    """Return the a room page Support debugging."""
    return render(request, 'support/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
