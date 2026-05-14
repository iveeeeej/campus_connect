from django.core.management import call_command
from django.test import TestCase

from apps.accounts.models import AccountStatus, Role, User
from apps.organizations.models import Organization


class SeedPhase1Tests(TestCase):
    def test_seed_phase1_is_rerunnable(self):
        call_command("seed_phase1", verbosity=0)
        call_command("seed_phase1", verbosity=0)

        self.assertEqual(Organization.objects.count(), 4)
        self.assertEqual(User.objects.filter(username="SUPER_ADMIN").count(), 1)
        self.assertEqual(User.objects.filter(is_shared_officer_account=True).count(), 4)

        usg_officer = User.objects.get(username="USG_OFFICER")
        self.assertEqual(usg_officer.role, Role.USG_OFFICER)
        self.assertEqual(usg_officer.organization.code, Organization.Code.USG)
        self.assertEqual(usg_officer.account_status, AccountStatus.APPROVED)
