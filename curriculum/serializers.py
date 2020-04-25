"""Curriculum serializers."""
from rest_framework import serializers

from .models import Course
from .models import Lesson
from .models import State


class StateSerializer(serializers.ModelSerializer):
    """State model serializer."""

    progress = serializers.CharField(
        read_only=True, source='get_progress_display')

    class Meta:
        """Meta class."""

        model = State
        fields = ('progress', )


class LessonSerializer(serializers.ModelSerializer):
    """Lesson model serializer."""

    course = serializers.StringRelatedField(read_only=True)
    reference = serializers.StringRelatedField(read_only=True)
    description = serializers.CharField(
        read_only=True, source='reference.description')
    sequence_number = serializers.IntegerField(read_only=True, min_value=0)
    active_bd = serializers.SerializerMethodField()
    state = serializers.SerializerMethodField()

    class Meta:
        """Meta class."""

        model = Lesson
        fields = '__all__'

    def _get_remix_bd(self, obj):
        """Get the remix block diagram if it exists."""
        user = self.context['request'].user

        return obj.block_diagrams.filter(user=user).last()

    def get_active_bd(self, obj):
        """Get the block diagram to load for this lesson."""
        bd = self._get_remix_bd(obj)
        if not bd:
            bd = obj.reference

        return bd.id

    def get_state(self, obj):
        """Get the state of this lesson."""
        bd = self._get_remix_bd(obj)
        if not bd:
            return None

        return StateSerializer(bd.state).data


class CourseSerializer(serializers.ModelSerializer):
    """Course model serializer."""

    lessons = LessonSerializer(read_only=True, many=True)

    class Meta:
        """Meta class."""

        model = Course
        fields = '__all__'
