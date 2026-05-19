from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from apps.organizations.models import Organization


class ScheduleItem(models.Model):
    class ItemType(models.TextChoices):
        EVENT = "EVENT", "Event"
        MEETING = "MEETING", "Meeting"

    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="schedule_items",
    )
    item_type = models.CharField(max_length=20, choices=ItemType.choices)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    venue = models.CharField(max_length=200)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    show_on_calendar = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_schedule_items",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["start_datetime", "title"]
        indexes = [
            models.Index(fields=["organization", "start_datetime"], name="schedule_org_start_idx"),
            models.Index(fields=["item_type", "start_datetime"], name="schedule_type_start_idx"),
            models.Index(fields=["show_on_calendar", "is_active"], name="schedule_visible_idx"),
        ]

    def clean(self):
        super().clean()
        if self.end_datetime and self.start_datetime and self.end_datetime <= self.start_datetime:
            raise ValidationError("End date/time must be later than start date/time.")

    def __str__(self):
        return f"{self.organization.code} {self.item_type}: {self.title}"
