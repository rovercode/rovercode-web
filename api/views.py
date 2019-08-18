"""API views."""
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, serializers, mixins

from mission_control.filters import BlockDiagramFilter
from mission_control.filters import RoverFilter
from mission_control.models import BlockDiagram
from mission_control.models import Rover
from mission_control.models import Tag
from mission_control.serializers import BlockDiagramSerializer
from mission_control.serializers import RoverSerializer
from mission_control.serializers import TagSerializer
from mission_control.serializers import UserSerializer

User = get_user_model()


class RoverViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows rovers to be viewed or edited.

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
    filterset_class = RoverFilter
    ordering_fields = ('name',)
    ordering = ('name',)
    search_fields = ('name',)

    def get_queryset(self):
        """List of rovers for the user."""
        owned_rovers = Rover.objects.filter(owner=self.request.user)
        shared_rovers = self.request.user.shared_rovers.all()
        return (owned_rovers | shared_rovers).distinct()

    def perform_create(self, serializer):
        """Perform the create operation."""
        user = self.request.user
        serializer.save(owner=user)


class BlockDiagramViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows block diagrams to be viewed or edited.

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
    filterset_class = BlockDiagramFilter
    ordering_fields = ('user', 'name')
    ordering = ('name',)
    search_fields = ('name',)

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


class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows users to be viewed.

    list:
        Return all users.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )
    ordering_fields = ('username',)
    ordering = ('username',)
    search_fields = ('username',)
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows tags to be viewed.

    retrieve:
        Return a tag instance.

    list:
        Return all tags.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated, )
    ordering_fields = ('name',)
    ordering = ('name',)
    search_fields = ('name',)
