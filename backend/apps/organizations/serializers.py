from rest_framework import serializers

from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = (
            "id",
            "code",
            "name",
            "organization_type",
            "is_active",
        )
        read_only_fields = fields
