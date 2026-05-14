from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Role, User
from .permissions import IsStudentRegistrationReviewer, IsSuperAdmin
from .serializers import (
    CampusConnectTokenObtainPairSerializer,
    RejectStudentSerializer,
    StudentCreateSerializer,
    StudentSerializer,
    StudentUpdateSerializer,
    UserSummarySerializer,
)
from .services import approve_student, deactivate_student, reject_student


class CampusConnectTokenObtainPairView(TokenObtainPairView):
    serializer_class = CampusConnectTokenObtainPairSerializer


class CurrentUserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        return Response(UserSummarySerializer(request.user).data)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role=Role.STUDENT).select_related("student_profile").order_by("-created_at")

    def get_permissions(self):
        if self.action in {"create", "update", "partial_update", "destroy", "deactivate"}:
            return [IsSuperAdmin()]
        if self.action in {"approve", "reject", "list", "retrieve"}:
            return [IsStudentRegistrationReviewer()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return StudentCreateSerializer
        if self.action in {"update", "partial_update"}:
            return StudentUpdateSerializer
        return StudentSerializer

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied("Student accounts must be deactivated, not deleted.")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(StudentSerializer(user).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(StudentSerializer(user).data)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        user = approve_student(self.get_object())
        return Response(StudentSerializer(user).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        serializer = RejectStudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = reject_student(self.get_object(), serializer.validated_data["reason"])
        return Response(StudentSerializer(user).data)

    @action(detail=True, methods=["post"])
    def deactivate(self, request, pk=None):
        user = deactivate_student(self.get_object())
        return Response(StudentSerializer(user).data)
