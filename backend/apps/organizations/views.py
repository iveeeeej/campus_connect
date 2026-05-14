from rest_framework.generics import ListAPIView

from .models import Organization
from .permissions import CanViewOrganizations
from .serializers import OrganizationSerializer


class OrganizationListView(ListAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [CanViewOrganizations]

    def get_queryset(self):
        return Organization.objects.filter(is_active=True)
