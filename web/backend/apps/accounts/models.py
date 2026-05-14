from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError
from django.db import models

from apps.organizations.models import Organization


class Role(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    USG_OFFICER = "USG_OFFICER", "USG Officer"
    ORG_OFFICER = "ORG_OFFICER", "Organization Officer"
    STUDENT = "STUDENT", "Student"
    SIGNATORY = "SIGNATORY", "Signatory"


class AccountStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"
    DEACTIVATED = "DEACTIVATED", "Deactivated"


class Course(models.TextChoices):
    IT = "IT", "Information Technology"
    BTLED = "BTLED", "Bachelor of Technology and Livelihood Education"
    BFPT = "BFPT", "Bachelor of Food Processing Technology"


class CampusConnectUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", Role.SUPER_ADMIN)
        extra_fields.setdefault("account_status", AccountStatus.APPROVED)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.STUDENT)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="users",
    )
    account_status = models.CharField(
        max_length=32,
        choices=AccountStatus.choices,
        default=AccountStatus.PENDING,
    )
    is_shared_officer_account = models.BooleanField(default=False)
    rejection_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CampusConnectUserManager()

    class Meta:
        indexes = [
            models.Index(fields=["role", "account_status"], name="accounts_user_role_status_idx"),
            models.Index(fields=["organization", "role"], name="accounts_user_org_role_idx"),
        ]

    def clean(self):
        super().clean()
        if self.role in {Role.USG_OFFICER, Role.ORG_OFFICER} and not self.organization_id:
            raise ValidationError("Officer accounts must be assigned to an organization.")
        if self.role == Role.USG_OFFICER and self.organization and self.organization.code != Organization.Code.USG:
            raise ValidationError("USG_OFFICER accounts must be assigned to the USG organization.")
        if self.role == Role.ORG_OFFICER and self.organization and self.organization.code == Organization.Code.USG:
            raise ValidationError("ORG_OFFICER accounts must be assigned to a non-USG organization.")
        if self.role == Role.STUDENT and self.organization_id:
            raise ValidationError("Student organization visibility is derived from profile course, not account organization.")

    @property
    def is_approved(self):
        return self.account_status == AccountStatus.APPROVED and self.is_active

    @property
    def is_super_admin_role(self):
        return self.role == Role.SUPER_ADMIN

    @property
    def is_officer_role(self):
        return self.role in {Role.USG_OFFICER, Role.ORG_OFFICER}

    @property
    def display_role_label(self):
        if self.role == Role.ORG_OFFICER and self.organization:
            return f"{self.organization.code} Officer"
        return self.get_role_display()


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )
    student_id = models.CharField(max_length=50, unique=True)
    middle_name = models.CharField(max_length=150, blank=True)
    course = models.CharField(max_length=20, choices=Course.choices)
    year_level = models.PositiveSmallIntegerField()
    section = models.CharField(max_length=50)
    school_id_qr_value = models.CharField(max_length=255, blank=True)
    face_embedding_registered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["student_id"]
        indexes = [
            models.Index(fields=["course"], name="student_profile_course_idx"),
            models.Index(fields=["student_id"], name="student_profile_student_id_idx"),
        ]

    def clean(self):
        super().clean()
        if self.user_id and self.user.role != Role.STUDENT:
            raise ValidationError("StudentProfile can only be attached to STUDENT users.")

    def __str__(self):
        return f"{self.student_id} - {self.user.get_full_name() or self.user.username}"

    @property
    def assigned_organization_code(self):
        return {
            Course.IT: Organization.Code.SITE,
            Course.BTLED: Organization.Code.PAFE,
            Course.BFPT: Organization.Code.AFPROTECH,
        }.get(self.course)

    @property
    def visible_organization_codes(self):
        codes = [Organization.Code.USG]
        assigned_code = self.assigned_organization_code
        if assigned_code:
            codes.append(assigned_code)
        return codes
