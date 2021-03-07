"""Mission Control serializers."""
import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from curriculum.models import Lesson
from curriculum.serializers import StateSerializer
from .fields import TagStringRelatedField
from .models import BlockDiagram
from .models import BlockDiagramBlogQuestion
from .models import BlogAnswer
from .models import Tag

NAME_REGEX = re.compile(r'\((?P<number>\d)\)$')

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        """Meta class."""

        model = User
        fields = ('username', )


class UserGuideSerializer(serializers.ModelSerializer):
    """User model serializer."""

    show_guide = serializers.BooleanField()

    class Meta:
        """Meta class."""

        model = User
        fields = ('show_guide', )


class BlockDiagramBlogQuestionReadSerializer(serializers.ModelSerializer):
    """BlockDiagramBlogQuestion model read serializer."""

    question = serializers.StringRelatedField(source='blog_question')
    answer = serializers.StringRelatedField(source='blog_answer')
    sequence_number = serializers.IntegerField(read_only=True, min_value=0)

    class Meta:
        """Meta class."""

        model = BlockDiagramBlogQuestion
        fields = ('id', 'question', 'answer', 'sequence_number')


class BlockDiagramBlogQuestionWriteSerializer(serializers.ModelSerializer):
    """BlockDiagramBlogQuestion model write serializer."""

    id = serializers.IntegerField()
    answer = serializers.CharField()

    class Meta:
        """Meta class."""

        model = BlockDiagramBlogQuestion
        fields = ('id', 'answer')


class BlockDiagramSerializer(serializers.ModelSerializer):
    """Block diagram model serializer."""

    admin_tags = serializers.StringRelatedField(read_only=True, many=True)
    owner_tags = TagStringRelatedField(required=False, many=True)
    tags = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    lesson = serializers.PrimaryKeyRelatedField(
        required=False, allow_null=True, queryset=Lesson.objects.all())
    state = StateSerializer(read_only=True)
    reference_of = serializers.PrimaryKeyRelatedField(read_only=True)
    flagged = serializers.BooleanField(read_only=True)
    blog_questions = BlockDiagramBlogQuestionReadSerializer(
        read_only=True, many=True)
    blog_answers = BlockDiagramBlogQuestionWriteSerializer(
        required=False, many=True)

    class Meta:
        """Meta class."""

        model = BlockDiagram
        fields = '__all__'

    @staticmethod
    def get_tags(obj):
        """All tags for the block diagram."""
        return [str(tag) for tag in obj.tags.all()]

    @staticmethod
    def validate_blog_answers(value):
        """Check that the answer is to a valid question."""
        ids = list(map(lambda answer: answer.get('id'), value))
        id_count = len(ids)
        obj_count = BlockDiagramBlogQuestion.objects.filter(id__in=ids).count()
        if id_count != obj_count:
            raise serializers.ValidationError(
                'At least one question does not exist for this block diagram',
            )

        return value

    def create(self, validated_data):
        """Check for name conflict and create unique name if necessary."""
        name = validated_data['name']
        owner_tags = validated_data.pop('owner_tags', [])

        match = NAME_REGEX.search(name)
        if match:
            number = int(match.group('number'))
        else:
            number = None

        user = self.context['request'].user
        while BlockDiagram.objects.filter(name=name, user=user).exists():
            if number is None:
                number = 1
                name = '{} ({})'.format(name, number)
            else:
                number += 1
                name = re.sub(NAME_REGEX, '({})'.format(number), name)

        validated_data['name'] = name

        block_diagram = super().create(validated_data)

        for tag in owner_tags:
            block_diagram.owner_tags.add(tag)

        return block_diagram

    def update(self, instance, validated_data):
        """Update answers to blog questions."""
        blog_answers = validated_data.pop('blog_answers', [])
        for answer in blog_answers:
            blog_answer, _ = BlogAnswer.objects.get_or_create(
                block_diagram_blog_question_id=answer['id'])
            blog_answer.answer = answer['answer']
            blog_answer.save()

        return super().update(instance, validated_data)


class TagSerializer(serializers.ModelSerializer):
    """Tag model serializer."""

    class Meta:
        """Meta class."""

        model = Tag
        fields = ('name', )
