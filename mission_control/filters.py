"""Mission Control filters."""
from django.db.models import Q
from django_filters.rest_framework import CharFilter
from django_filters.rest_framework import FilterSet
from django_filters.rest_framework import NumberFilter

from .models import BlockDiagram
from .models import Rover


class RoverFilter(FilterSet):
    """Filterset for the Rover model."""

    client_id = CharFilter(field_name='oauth_application__client_id')

    class Meta:
        """Meta class."""

        model = Rover
        fields = ['name', 'client_id']


class BlockDiagramFilter(FilterSet):
    """Filterset for the BlockDiagram model."""

    tag = CharFilter(
        method='filter_tags',
    )
    user__not = NumberFilter(field_name='user', exclude=True)

    class Meta:
        """Meta class."""

        model = BlockDiagram
        fields = ['name', 'tag', 'user', 'user__not']

    @staticmethod
    def filter_tags(queryset, _, value):
        """Use all tags when filtering."""
        tags = value.split(',')
        return queryset.filter(
            Q(owner_tags__name__in=tags) | Q(admin_tags__name__in=tags)
        ).distinct()
