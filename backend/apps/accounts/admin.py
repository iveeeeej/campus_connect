from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import StudentProfile, User


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile
    can_delete = False
    extra = 0


@admin.register(User)
class CampusConnectUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Campus Connect",
            {
                "fields": (
                    "role",
                    "organization",
                    "account_status",
                    "is_shared_officer_account",
                    "rejection_reason",
                )
            },
        ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "Campus Connect",
            {
                "fields": (
                    "role",
                    "organization",
                    "account_status",
                    "is_shared_officer_account",
                )
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "role",
        "organization",
        "account_status",
        "is_active",
        "is_staff",
    )
    list_filter = ("role", "account_status", "organization", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")
    inlines = [StudentProfileInline]


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("student_id", "user", "course", "year_level", "section", "face_embedding_registered")
    list_filter = ("course", "year_level", "face_embedding_registered")
    search_fields = ("student_id", "user__username", "user__first_name", "user__last_name", "user__email")
