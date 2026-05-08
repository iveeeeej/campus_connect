from django.db import transaction

from apps.organizations.models import Organization

from .models import AccountStatus, Course, Role, StudentProfile, User


COURSE_TO_ORGANIZATION_CODE = {
    Course.IT: Organization.Code.SITE,
    Course.BTLED: Organization.Code.PAFE,
    Course.BFPT: Organization.Code.AFPROTECH,
}


def student_visible_organization_codes(course):
    codes = [Organization.Code.USG]
    assigned_code = COURSE_TO_ORGANIZATION_CODE.get(course)
    if assigned_code:
        codes.append(assigned_code)
    return codes


@transaction.atomic
def create_student_account(validated_data):
    profile_data = validated_data.pop("student_profile")
    password = validated_data.pop("password")
    user = User(
        **validated_data,
        role=Role.STUDENT,
        account_status=AccountStatus.PENDING,
        is_active=True,
    )
    user.set_password(password)
    user.full_clean()
    user.save()

    profile = StudentProfile(user=user, **profile_data)
    profile.full_clean()
    profile.save()
    return user


@transaction.atomic
def update_student_account(user, validated_data):
    profile_data = validated_data.pop("student_profile", None)
    password = validated_data.pop("password", None)

    for field, value in validated_data.items():
        setattr(user, field, value)
    if password:
        user.set_password(password)
    user.full_clean()
    user.save()

    if profile_data is not None:
        profile = user.student_profile
        for field, value in profile_data.items():
            setattr(profile, field, value)
        profile.full_clean()
        profile.save()
    return user


def approve_student(user):
    user.account_status = AccountStatus.APPROVED
    user.rejection_reason = ""
    user.is_active = True
    user.full_clean()
    user.save(update_fields=["account_status", "rejection_reason", "is_active", "updated_at"])
    return user


def reject_student(user, reason):
    user.account_status = AccountStatus.REJECTED
    user.rejection_reason = reason
    user.is_active = False
    user.full_clean()
    user.save(update_fields=["account_status", "rejection_reason", "is_active", "updated_at"])
    return user


def deactivate_student(user):
    user.account_status = AccountStatus.DEACTIVATED
    user.is_active = False
    user.full_clean()
    user.save(update_fields=["account_status", "is_active", "updated_at"])
    return user
