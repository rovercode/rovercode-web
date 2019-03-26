"""Mission Control filters."""
from django_filters.rest_framework import CharFilter
from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import NumberFilter

from .models import BlockDiagram
from .models import Rover


class RoverFilter(FilterSet):
    """Filterset for the Rover model."""

    client_id = CharFilter(name='oauth_application__client_id')

    class Meta:
        """Meta class."""

        model = Rover
        fields = ['name', 'client_id']


class BlockDiagramFilter(FilterSet):
    """Filterset for the BlockDiagram model."""

    user__not = NumberFilter(field_name='user', exclude=True)

    class Meta:
        """Meta class."""

        model = BlockDiagram
        fields = ['name', 'user', 'user__not']
