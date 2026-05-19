from rest_framework import serializers

from .models import ScheduleItem


class CalendarScheduleItemSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(source="organization.code", read_only=True)
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = ScheduleItem
        fields = (
            "id",
            "item_type",
            "title",
            "organization",
            "organization_name",
            "venue",
            "start_datetime",
            "end_datetime",
        )
        read_only_fields = fields
