"""Mission Control filters."""
from django_filters.rest_framework import CharFilter
from django_filters.rest_framework import FilterSet

from .models import Rover


class RoverFilter(FilterSet):
    """Filterset for the Rover model."""

    client_id = CharFilter(name='oauth_application__client_id')

    class Meta:
        """Meta class."""

        model = Rover
        fields = ['name', 'client_id']
