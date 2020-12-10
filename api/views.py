"""API views."""
import json
import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.template import loader
from rest_framework import viewsets, permissions, serializers, mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from zenpy import Zenpy
from zenpy.lib.api_objects import Ticket
from zenpy.lib.api_objects import User as ZendeskUser

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
ZENDESK = Zenpy(**{
    'email': settings.ZENDESK_EMAIL,
    'token': settings.ZENDESK_TOKEN,
    'subdomain': settings.ZENDESK_SUBDOMAIN,
})


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

    serializer_class = BlockDiagramSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filterset_class = BlockDiagramFilter
    ordering_fields = ('user', 'name')
    ordering = ('name',)
    search_fields = ('name', 'user__username')

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

    @staticmethod
    def _is_over_limit(request):
        """Determine if the user is over the limit of programs."""
        claims = api_settings.JWT_DECODE_HANDLER(request.auth)
        tier = claims.get('tier', 1)
        user_program_count = BlockDiagram.objects.filter(
            user=request.user
        ).count()
        free_limit = settings.FREE_TIER_PROGRAM_LIMIT
        if tier == 1 and user_program_count >= free_limit:
            return True

        return False

    def get_queryset(self):
        """Return the objects available for the operation."""
        if self.action in ['update', 'partial_update', 'destroy']:
            return BlockDiagram.objects.filter(user=self.request.user)
        if self.action == 'list':
            support = User.objects.get(email=settings.SUPPORT_CONTACT)

            bds = BlockDiagram.objects.filter(reference_of=None)

            if self.request.user == support:
                return bds

            return bds.exclude(user=support)

        claims = api_settings.JWT_DECODE_HANDLER(self.request.auth)
        return BlockDiagram.objects.filter(
            Q(reference_of__tier__lte=claims.get('tier', 1)) |
            Q(reference_of=None)
        )

    def perform_create(self, serializer):
        """Perform the create operation."""
        if self._is_over_limit(self.request):
            raise serializers.ValidationError(
                'You are over the limit of programs allowed.',
            )

        user = self.request.user
        serializer.save(user=user)

    @staticmethod
    @action(detail=True, methods=['POST'])
    def remix(request, **kwargs):
        """Copy the block diagram for the user."""
        if BlockDiagramViewSet._is_over_limit(request):
            raise serializers.ValidationError(
                'You are over the limit of programs allowed.',
            )

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

    @staticmethod
    @action(detail=True, methods=['POST'])
    def report(request, **kwargs):
        """Report issues with block diagram."""
        bd = get_object_or_404(BlockDiagram, pk=kwargs.get('pk'))
        description = request.data.get('description')

        user = request.user

        source_id = bd.id
        source_name = bd.name

        bd.pk = None
        bd.name = f'{source_id} - {bd.name}'
        support = User.objects.get(email=settings.SUPPORT_CONTACT)
        bd.user = support

        if BlockDiagram.objects.filter(user=support, name=bd.name).exists():
            bd.name = BlockDiagramViewSet._find_unique_name(bd.name, support)
        bd.save()

        body = loader.render_to_string('email/issue_report.html', {
            'user': user,
            'id': source_id,
            'name': source_name,
            'description': description,
        })

        ZENDESK.tickets.create(
            Ticket(
                subject='Program Issue Reported',
                description=body,
                type='problem',
                tags=['program'],
                requester=ZendeskUser(name=user.username, email=user.email),
            )
        )

        SUMO_LOGGER.info(json.dumps({
            'event': 'report',
            'userId': user.id,
            'sourceProgramId': source_id,
            'newProgramId': bd.id,
        }))

        return Response(status.HTTP_200_OK)


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
        if self.get_object().id != self.request.user.id:
            raise serializers.ValidationError('You may only modify yourself')
        serializer.save()

    @staticmethod
    @action(detail=True, methods=['GET'])
    def stats(request, **kwargs):
        """Get user statistics."""
        user = get_object_or_404(User, pk=kwargs.get('pk'))
        if user != request.user:
            return HttpResponseForbidden()

        stats = {
            'block_diagram': {
                'count': BlockDiagram.objects.filter(user=user).count(),
                'limit': settings.FREE_TIER_PROGRAM_LIMIT,
            },
        }

        return JsonResponse(stats)


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
