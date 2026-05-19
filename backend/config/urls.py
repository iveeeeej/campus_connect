from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.accounts.views import CampusConnectTokenObtainPairView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/token/", CampusConnectTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/accounts/", include("apps.accounts.urls")),
    path("api/calendar/", include("apps.scheduling.urls")),
    path("api/organizations/", include("apps.organizations.urls")),
]



