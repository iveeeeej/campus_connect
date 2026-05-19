from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView

from apps.accounts.permissions import IsApprovedAuthenticated, IsSuperAdmin
from apps.organizations.models import Organization

from .models import ScheduleItem
from .serializers import CalendarScheduleItemSerializer


class SuperAdminCalendarScheduleListView(ListAPIView):
    serializer_class = CalendarScheduleItemSerializer
    permission_classes = [IsApprovedAuthenticated, IsSuperAdmin]

    def get_queryset(self):
        queryset = ScheduleItem.objects.filter(
            is_active=True,
            show_on_calendar=True,
        ).select_related("organization")

        organization = self.request.query_params.get("organization", "all").strip().upper()
        if organization in {"", "ALL"}:
            return queryset

        if organization not in Organization.Code.values:
            raise ValidationError(
                {
                    "organization": (
                        "Use 'all', 'USG', 'SITE', 'PAFE', or 'AFPROTECH'."
                    )
                }
            )

        return queryset.filter(organization__code=organization)
