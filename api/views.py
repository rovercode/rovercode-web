"""API views."""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, serializers

from mission_control.filters import RoverFilter
from mission_control.models import Rover, BlockDiagram
from mission_control.serializers import RoverSerializer, BlockDiagramSerializer


class RoverViewSet(viewsets.ModelViewSet):
    """API endpoint that allows rovers to be viewed or edited.

    retrieve:
        Return a rover instance.

    list:
        Return all rovers.

    create:
        Register a new rover.

    delete:
        Remove an existing rover.

    partial_update:
        Update one or more fields on an existing rover.

    update:
        Update a rover.
    """

    serializer_class = RoverSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (DjangoFilterBackend,)
    filter_class = RoverFilter

    def get_queryset(self):
        """The list of rovers for the user."""
        return Rover.objects.filter(owner=self.request.user.id)

    def perform_create(self, serializer):
        """Perform the create operation."""
        user = self.request.user
        serializer.save(owner=user)


class BlockDiagramViewSet(viewsets.ModelViewSet):
    """API endpoint that allows block diagrams to be viewed or edited.

    retrieve:
        Return a block diagram instance.

    list:
        Return all block diagrams.

    create:
        Create a new block diagram.

    delete:
        Remove an existing block diagram.

    partial_update:
        Update one or more fields on an existing block diagram.

    update:
        Update a block diagram.
    """

    queryset = BlockDiagram.objects.all()
    serializer_class = BlockDiagramSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('user', 'name')

    def perform_create(self, serializer):
        """Perform the create operation."""
        user = self.request.user
        serializer.save(user=user)

    def perform_update(self, serializer):
        """Perform the update operation."""
        if self.get_object().user.id is not self.request.user.id:
            raise serializers.ValidationError(
                'You may only modify your own block diagrams')
        serializer.save()
