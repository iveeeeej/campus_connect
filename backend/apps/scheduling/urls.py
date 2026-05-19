from django.urls import path

from .views import SuperAdminCalendarScheduleListView


urlpatterns = [
    path("", SuperAdminCalendarScheduleListView.as_view(), name="calendar-schedule-list"),
]
