"""API views."""
import json
import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, permissions, serializers, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from curriculum.models import Course
from curriculum.models import Lesson
from curriculum.models import ProgressState
from curriculum.models import State
from curriculum.serializers import CourseSerializer
from curriculum.serializers import LessonSerializer
from mission_control.filters import BlockDiagramFilter
from mission_control.models import BlockDiagram
from mission_control.models import Tag
from mission_control.serializers import BlockDiagramSerializer
from mission_control.serializers import TagSerializer
from mission_control.serializers import UserGuideSerializer

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

    @staticmethod
    def _find_unique_name(name, user):
        """Find a unique name for the block diagram."""
        number = 1
        while True:
            unique = f'{name} ({number})'
            if BlockDiagram.objects.filter(user=user, name=unique).exists():
                number += 1
            else:
                return unique

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

        user = request.user
        if bd.user == user:
            raise serializers.ValidationError(
                'You are not allowed to remix your own program.',
            )

        source_id = bd.id
        try:
            bd.lesson = bd.reference_of
            bd.state = State.objects.create(progress=ProgressState.IN_PROGRESS)
        except ObjectDoesNotExist:
            # Source is not a lesson reference
            pass

        bd.pk = None
        bd.user = user

        if BlockDiagram.objects.filter(user=user, name=bd.name).exists():
            bd.name = BlockDiagramViewSet._find_unique_name(bd.name, user)
        bd.save()

        SUMO_LOGGER.info(json.dumps({
            'event': 'remix',
            'userId': user.id,
            'sourceProgramId': source_id,
            'newProgramId': bd.id,
        }))

        return Response(
            BlockDiagramSerializer(bd).data, status.HTTP_200_OK)


class UserViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    API endpoint that allows user to be modified.

    update:
        Update user.

    partial_update:
        Update user.
    """

    queryset = User.objects.all()
    serializer_class = UserGuideSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = []

    def perform_update(self, serializer):
        """Perform the update operation."""
        if self.get_object().id is not self.request.user.id:
            raise serializers.ValidationError('You may only modify yourself')
        serializer.save()


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
