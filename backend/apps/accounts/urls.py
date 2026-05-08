from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CurrentUserViewSet, StudentViewSet


router = DefaultRouter()
router.register("me", CurrentUserViewSet, basename="current-user")
router.register("students", StudentViewSet, basename="student")


urlpatterns = [
    path("", include(router.urls)),
]
