from django.test import TestCase

from apps.accounts.models import AccountStatus, Role, User
from apps.accounts.permissions import can_manage_organization_record
from apps.organizations.models import Organization


class OrganizationPermissionTests(TestCase):
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

    def test_officer_can_manage_only_own_organization(self):
        officer = User.objects.create_user(
            username="SITE_OFFICER",
            password="test-pass",
            role=Role.ORG_OFFICER,
            organization=self.site,
            account_status=AccountStatus.APPROVED,
            is_shared_officer_account=True,
        )

        self.assertTrue(can_manage_organization_record(officer, self.site))
        self.assertFalse(can_manage_organization_record(officer, self.usg))

    def test_super_admin_can_manage_all_organizations(self):
        super_admin = User.objects.create_superuser(
            username="SUPER_ADMIN",
            password="test-pass",
        )

        self.assertTrue(can_manage_organization_record(super_admin, self.usg))
        self.assertTrue(can_manage_organization_record(super_admin, self.site))
