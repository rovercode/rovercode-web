"""API views."""
import json
import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from rest_framework import viewsets, permissions, serializers, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from curriculum.models import Course
from curriculum.models import Lesson
from curriculum.serializers import CourseSerializer
from curriculum.serializers import LessonSerializer
from mission_control.filters import BlockDiagramFilter
from mission_control.models import BlockDiagram
from mission_control.models import Tag
from mission_control.serializers import BlockDiagramSerializer
from mission_control.serializers import TagSerializer
from mission_control.serializers import UserSerializer

User = get_user_model()

SUMO_LOGGER = logging.getLogger('sumo')


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

    @staticmethod
    @action(detail=True, methods=['POST'])
    def remix(request, **kwargs):
        """Copy the block diagram for the user."""
        bd = get_object_or_404(BlockDiagram, pk=kwargs.get('pk'))
        if bd.user == request.user:
            raise serializers.ValidationError(
                'You are not allowed to remix your own program.',
            )

        source_id = bd.id
        try:
            bd.lesson = bd.reference_of
        except ObjectDoesNotExist:
            # Source is not a lesson reference
            pass

        bd.pk = None
        bd.user = request.user
        try:
            bd.save()
        except IntegrityError:
            raise serializers.ValidationError(
                'You have already remixed this program.',
            )

        SUMO_LOGGER.info(json.dumps({
            'event': 'remix',
            'userId': request.user.id,
            'sourceProgramId': source_id,
            'newProgramId': bd.id,
        }))

        return Response(
            BlockDiagramSerializer(bd).data, status.HTTP_200_OK)


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
    pagination_class = None


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows courses to be viewed.

    retrieve:
        Return a course instance.

    list:
        Return all courses.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (permissions.IsAuthenticated, )
    ordering_fields = ('name',)
    ordering = ('name',)
    search_fields = ('name',)


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows lessons to be viewed.

    retrieve:
        Return a lesson instance.

    list:
        Return all lessons.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (permissions.IsAuthenticated, )
    ordering_fields = ('reference', 'course')
    ordering = ('reference',)
    search_fields = ('reference__name', 'course__name')
