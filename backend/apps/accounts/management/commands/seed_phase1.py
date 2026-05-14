from django.core.management.base import BaseCommand
from django.db import transaction

from apps.accounts.models import AccountStatus, Role, User
from apps.organizations.models import Organization


ORGANIZATIONS = {
    Organization.Code.USG: {
        "name": "University Student Government",
        "organization_type": Organization.Type.UNIVERSITY_WIDE,
    },
    Organization.Code.SITE: {
        "name": "Society of Information Technology Enthusiasts",
        "organization_type": Organization.Type.COURSE_DEPARTMENT,
    },
    Organization.Code.PAFE: {
        "name": "PAFE",
        "organization_type": Organization.Type.COURSE_DEPARTMENT,
    },
    Organization.Code.AFPROTECH: {
        "name": "AFPROTECH",
        "organization_type": Organization.Type.COURSE_DEPARTMENT,
    },
}

DEFAULT_ACCOUNTS = [
    {
        "username": "SUPER_ADMIN",
        "email": "super_admin@campusconnect.local",
        "role": Role.SUPER_ADMIN,
        "organization_code": None,
        "is_staff": True,
        "is_superuser": True,
        "is_shared_officer_account": False,
    },
    {
        "username": "USG_OFFICER",
        "email": "usg_officer@campusconnect.local",
        "role": Role.USG_OFFICER,
        "organization_code": Organization.Code.USG,
        "is_staff": False,
        "is_superuser": False,
        "is_shared_officer_account": True,
    },
    {
        "username": "SITE_OFFICER",
        "email": "site_officer@campusconnect.local",
        "role": Role.ORG_OFFICER,
        "organization_code": Organization.Code.SITE,
        "is_staff": False,
        "is_superuser": False,
        "is_shared_officer_account": True,
    },
    {
        "username": "PAFE_OFFICER",
        "email": "pafe_officer@campusconnect.local",
        "role": Role.ORG_OFFICER,
        "organization_code": Organization.Code.PAFE,
        "is_staff": False,
        "is_superuser": False,
        "is_shared_officer_account": True,
    },
    {
        "username": "AFPROTECH_OFFICER",
        "email": "afprotech_officer@campusconnect.local",
        "role": Role.ORG_OFFICER,
        "organization_code": Organization.Code.AFPROTECH,
        "is_staff": False,
        "is_superuser": False,
        "is_shared_officer_account": True,
    },
]


class Command(BaseCommand):
    help = "Seed Phase 1 organizations and default shared accounts."

    def add_arguments(self, parser):
        parser.add_argument(
            "--default-password",
            default="CampusConnect@12345",
            help="Password used for newly created default accounts.",
        )
        parser.add_argument(
            "--reset-passwords",
            action="store_true",
            help="Reset passwords for existing default accounts.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        default_password = options["default_password"]
        reset_passwords = options["reset_passwords"]

        organizations = self.seed_organizations()
        self.seed_accounts(organizations, default_password, reset_passwords)

        self.stdout.write(self.style.SUCCESS("Phase 1 seed data is ready."))

    def seed_organizations(self):
        organizations = {}
        for code, defaults in ORGANIZATIONS.items():
            organization, created = Organization.objects.update_or_create(
                code=code,
                defaults={**defaults, "is_active": True},
            )
            organizations[code] = organization
            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} organization {code}")
        return organizations

    def seed_accounts(self, organizations, default_password, reset_passwords):
        for account_data in DEFAULT_ACCOUNTS:
            username = account_data["username"]
            organization_code = account_data["organization_code"]
            organization = organizations.get(organization_code) if organization_code else None

            user, created = User.objects.get_or_create(username=username)
            user.email = account_data["email"]
            user.role = account_data["role"]
            user.organization = organization
            user.account_status = AccountStatus.APPROVED
            user.is_active = True
            user.is_staff = account_data["is_staff"]
            user.is_superuser = account_data["is_superuser"]
            user.is_shared_officer_account = account_data["is_shared_officer_account"]
            user.rejection_reason = ""

            if created or reset_passwords:
                user.set_password(default_password)

            user.full_clean()
            user.save()

            action = "Created" if created else "Updated"
            self.stdout.write(f"{action} account {username}")
