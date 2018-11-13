"""Mission Control serializers."""
from rest_framework import serializers

from .models import SupportRequest, AbuseReport

class SupportRequestSerializer(serializers.ModelSerializer):
    """Support request model serializer."""

    class Meta:
        """Meta class."""

        model = SupportRequest
        fields = '__all__'
        read_only_fields = ('owner', 'creation_time')

class AbuseReportSerializer(serializers.ModelSerializer):
    """Support request model serializer."""

    class Meta:
        """Meta class."""

        model = AbuseReport
        fields = '__all__'
        read_only_fields = ('reporter', 'accused_user', 'transcript', 'support_request')