from django.contrib import admin

from .models import ScheduleItem


@admin.register(ScheduleItem)
class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "item_type",
        "organization",
        "venue",
        "start_datetime",
        "end_datetime",
        "show_on_calendar",
        "is_active",
    )
    list_filter = ("item_type", "organization", "show_on_calendar", "is_active")
    search_fields = ("title", "venue", "description")
