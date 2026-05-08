from django.urls import reverse
from rest_framework.test import APITestCase

from apps.accounts.models import AccountStatus, Role, StudentProfile, User
from apps.organizations.models import Organization


class StudentApiTests(APITestCase):
    def setUp(self):
        self.usg = Organization.objects.create(
            code=Organization.Code.USG,
            name="University Student Government",
            organization_type=Organization.Type.UNIVERSITY_WIDE,
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
            is_shared_officer_account=True,
        )

    def test_super_admin_can_create_student(self):
        self.client.force_authenticate(self.super_admin)
        response = self.client.post(
            reverse("student-list"),
            {
                "username": "2026-0001",
                "password": "StrongPass123!",
                "email": "student@example.com",
                "first_name": "Ada",
                "last_name": "Lovelace",
                "student_profile": {
                    "student_id": "2026-0001",
                    "middle_name": "",
                    "course": "IT",
                    "year_level": 1,
                    "section": "A",
                    "school_id_qr_value": "2026-0001",
                },
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["account_status"], AccountStatus.PENDING)

    def test_usg_officer_can_approve_student(self):
        student = User.objects.create_user(
            username="2026-0002",
            password="test-pass",
            role=Role.STUDENT,
            account_status=AccountStatus.PENDING,
        )
        StudentProfile.objects.create(
            user=student,
            student_id="2026-0002",
            course="IT",
            year_level=1,
            section="A",
            school_id_qr_value="2026-0002",
        )

        self.client.force_authenticate(self.usg_officer)
        response = self.client.post(reverse("student-approve", args=[student.id]))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["account_status"], AccountStatus.APPROVED)
