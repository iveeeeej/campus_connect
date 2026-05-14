from rest_framework.permissions import BasePermission

from .models import AccountStatus, Role


def is_super_admin(user):
    return bool(user and user.is_authenticated and user.role == Role.SUPER_ADMIN)


def is_usg_officer(user):
    return bool(user and user.is_authenticated and user.role == Role.USG_OFFICER)


def is_org_officer(user):
    return bool(user and user.is_authenticated and user.role == Role.ORG_OFFICER)


def is_student_manager(user):
    return bool(
        user
        and user.is_authenticated
        and user.account_status == AccountStatus.APPROVED
        and user.role in {Role.SUPER_ADMIN, Role.USG_OFFICER}
    )


def can_manage_organization_record(user, organization):
    if not user or not user.is_authenticated or user.account_status != AccountStatus.APPROVED:
        return False
    if user.role == Role.SUPER_ADMIN:
        return True
    if user.role in {Role.USG_OFFICER, Role.ORG_OFFICER}:
        return bool(user.organization_id and organization and user.organization_id == organization.id)
    return False


class IsApprovedAuthenticated(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and user.account_status == AccountStatus.APPROVED and user.is_active)


class IsStudentManager(BasePermission):
    def has_permission(self, request, view):
        return is_student_manager(request.user)


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return is_super_admin(request.user)


class IsStudentRegistrationReviewer(BasePermission):
    message = "Only SUPER_ADMIN and approved USG_OFFICER accounts may review student registrations."

    def has_permission(self, request, view):
        return is_student_manager(request.user)

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
