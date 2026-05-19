from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APITestCase

from apps.accounts.models import AccountStatus, Role, User
from apps.organizations.models import Organization
from apps.scheduling.models import ScheduleItem


class SuperAdminCalendarTests(APITestCase):
    def setUp(self):
        self.usg = Organization.objects.create(
            code=Organization.Code.USG,
            name="University Student Government",
            organization_type=Organization.Type.UNIVERSITY_WIDE,
        )
        self.site = Organization.objects.create(
            code=Organization.Code.SITE,
            name="Society of Information Technology Enthusiasts",
            organization_type=Organization.Type.COURSE_DEPARTMENT,
        )
        self.super_admin = User.objects.create_superuser(
            username="SUPER_ADMIN",
            password="test-pass",
        )
        self.usg_officer = User.objects.create_user(
            username="USG_OFFICER",
            password="test-pass",
            role=Role.USG_OFFICER,
            organization=self.usg,
            account_status=AccountStatus.APPROVED,
        )

        start = timezone.now() + timezone.timedelta(days=1)
        self.usg_event = ScheduleItem.objects.create(
            organization=self.usg,
            item_type=ScheduleItem.ItemType.EVENT,
            title="USG General Assembly",
            venue="Covered Court",
            start_datetime=start,
            end_datetime=start + timezone.timedelta(hours=2),
            created_by=self.super_admin,
        )
        self.site_meeting = ScheduleItem.objects.create(
            organization=self.site,
            item_type=ScheduleItem.ItemType.MEETING,
            title="SITE Planning Meeting",
            venue="IT Laboratory",
            start_datetime=start + timezone.timedelta(days=1),
            end_datetime=start + timezone.timedelta(days=1, hours=1),
            created_by=self.super_admin,
        )
        ScheduleItem.objects.create(
            organization=self.site,
            item_type=ScheduleItem.ItemType.MEETING,
            title="Hidden Internal Meeting",
            venue="IT Laboratory",
            start_datetime=start + timezone.timedelta(days=2),
            end_datetime=start + timezone.timedelta(days=2, hours=1),
            show_on_calendar=False,
            created_by=self.super_admin,
        )

    def test_super_admin_can_view_all_visible_calendar_items(self):
        self.client.force_authenticate(self.super_admin)

        response = self.client.get(reverse("calendar-schedule-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        titles = {item["title"] for item in response.data}
        self.assertEqual(titles, {"USG General Assembly", "SITE Planning Meeting"})

    def test_super_admin_can_filter_calendar_by_organization(self):
        self.client.force_authenticate(self.super_admin)

        response = self.client.get(reverse("calendar-schedule-list"), {"organization": "SITE"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "SITE Planning Meeting")
        self.assertEqual(response.data[0]["organization"], Organization.Code.SITE)

    def test_super_admin_gets_validation_error_for_unknown_organization_filter(self):
        self.client.force_authenticate(self.super_admin)

        response = self.client.get(reverse("calendar-schedule-list"), {"organization": "UNKNOWN"})

        self.assertEqual(response.status_code, 400)
        self.assertIn("organization", response.data["error"])

    def test_non_super_admin_cannot_use_super_admin_calendar_endpoint(self):
        self.client.force_authenticate(self.usg_officer)

        response = self.client.get(reverse("calendar-schedule-list"))

        self.assertEqual(response.status_code, 403)

