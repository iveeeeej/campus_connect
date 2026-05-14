from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.organizations.serializers import OrganizationSerializer

from .models import AccountStatus, Role, StudentProfile, User
from .services import create_student_account, student_visible_organization_codes, update_student_account


class CampusConnectTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        if self.user.account_status in {AccountStatus.REJECTED, AccountStatus.DEACTIVATED}:
            raise serializers.ValidationError("This account is not allowed to sign in.")

        data["user"] = UserSummarySerializer(self.user).data
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = user.role
        token["account_status"] = user.account_status
        token["organization"] = user.organization.code if user.organization else None
        return token


class StudentProfileSerializer(serializers.ModelSerializer):
    assigned_organization_code = serializers.CharField(read_only=True)
    visible_organization_codes = serializers.ListField(
        child=serializers.CharField(),
        read_only=True,
    )

    class Meta:
        model = StudentProfile
        fields = (
            "student_id",
            "middle_name",
            "course",
            "year_level",
            "section",
            "school_id_qr_value",
            "face_embedding_registered",
            "assigned_organization_code",
            "visible_organization_codes",
        )


class StudentProfileWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = (
            "student_id",
            "middle_name",
            "course",
            "year_level",
            "section",
            "school_id_qr_value",
            "face_embedding_registered",
        )
        extra_kwargs = {
            "face_embedding_registered": {"required": False},
            "school_id_qr_value": {"required": False, "allow_blank": True},
            "middle_name": {"required": False, "allow_blank": True},
        }


class UserSummarySerializer(serializers.ModelSerializer):
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "organization",
            "account_status",
            "is_shared_officer_account",
            "display_role_label",
            "is_active",
        )
        read_only_fields = fields


class StudentSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "account_status",
            "rejection_reason",
            "is_active",
            "student_profile",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class StudentCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    student_profile = StudentProfileWriteSerializer()

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "student_profile",
        )

    def create(self, validated_data):
        return create_student_account(validated_data)


class StudentUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
        validators=[validate_password],
    )
    student_profile = StudentProfileWriteSerializer(required=False)

    class Meta:
        model = User
        fields = (
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "student_profile",
        )
        extra_kwargs = {
            "username": {"required": False},
            "email": {"required": False},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def update(self, instance, validated_data):
        return update_student_account(instance, validated_data)


class RejectStudentSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=1000, allow_blank=False, trim_whitespace=True)


class StudentVisibilitySerializer(serializers.Serializer):
    course = serializers.CharField()
    visible_organization_codes = serializers.SerializerMethodField()

    def get_visible_organization_codes(self, obj):
        return student_visible_organization_codes(obj["course"])
