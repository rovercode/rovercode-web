"""Mission Control serializers."""
import re

from django.contrib.auth import get_user_model
from rest_framework import serializers

from curriculum.serializers import StateSerializer
from .fields import TagStringRelatedField
from .models import BlockDiagram
from .models import Tag

NAME_REGEX = re.compile(r'\((?P<number>\d)\)$')

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User model serializer."""

    class Meta:
        """Meta class."""

        model = User
        fields = ('username', )


class BlockDiagramSerializer(serializers.ModelSerializer):
    """Block diagram model serializer."""

    admin_tags = serializers.StringRelatedField(read_only=True, many=True)
    owner_tags = TagStringRelatedField(required=False, many=True)
    tags = serializers.SerializerMethodField()
    user = UserSerializer(read_only=True)
    lesson = serializers.StringRelatedField(read_only=True)
    state = StateSerializer(read_only=True)
    reference_of = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """Meta class."""

        model = BlockDiagram
        fields = '__all__'

    @staticmethod
    def get_tags(obj):
        """All tags for the block diagram."""
        return [str(tag) for tag in obj.tags.all()]

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


class TagSerializer(serializers.ModelSerializer):
    """Tag model serializer."""

    class Meta:
        """Meta class."""

        model = Tag
        fields = ('name', )
