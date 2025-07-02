from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from carbon_restapi.trips.models import Employee, Status, Trip, Mission, Transport
from carbon_restapi.trips.serializers import (
    TripSerializer,
    MissionSerializer,
    EmployeeSerializer,
    StatusSerializer,
    TransportSerializer,
)
from carbon_restapi.trips.permissions import (
    IsViewEmployeePermission,
    IsViewTripPermission,
    IsAddTripPermission,
    IsDeleteTripPermission,
    IsModifyTripPermission,
    IsViewMissionPermission,
    IsAddMissionPermission,
    IsDeleteMissionPermission,
    IsModifyMissionPermission,
    IsModifyEmployeePermission,
)

from carbon_restapi.trips.filters import TripFilter


class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    swagger_tags = ['status']
    http_method_names = ['get', 'head', 'options']
    permission_classes = [IsAuthenticated]
    serializer_class = StatusSerializer
    queryset = Status.objects.all()


class EmployeeViewSet(viewsets.ModelViewSet):
    swagger_tags = ['employees']
    http_method_names = ['get', 'put', 'patch', 'head', 'options']
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.select_related('status').all()

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated(), IsViewEmployeePermission()]
        if self.action in ('update', 'partial_update'):
            return [IsAuthenticated(), IsModifyEmployeePermission()]
        return [IsAuthenticated()]
    

class TransportViewSet(viewsets.ReadOnlyModelViewSet):
    swagger_tags = ['transports']
    http_method_names = ['get', 'head', 'options']
    permission_classes = [IsAuthenticated]
    serializer_class = TransportSerializer
    queryset = Transport.objects.all()


class TripViewSet(viewsets.ModelViewSet):
    swagger_tags = ['trips']
    permission_classes = [IsAuthenticated]
    serializer_class = TripSerializer
    queryset = Trip.objects.select_related('mission', 'transport').all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TripFilter
    ordering = ['-mission__start_date']  # descending order

    def get_permissions(self):
        perms_map = {
            'list': [IsAuthenticated(), IsViewTripPermission()],
            'create': [IsAuthenticated(), IsAddTripPermission()],
            'update': [IsAuthenticated(), IsModifyTripPermission()],
            'partial_update': [IsAuthenticated(), IsModifyTripPermission()],
            'destroy': [IsAuthenticated(), IsDeleteTripPermission()],
        }
        return perms_map.get(self.action, [IsAuthenticated()])

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'group') and user.group.group_name == 'MISSIONMANAGER':
            return self.queryset
        if hasattr(user, 'employee'):
            return self.queryset.filter(mission__employee=user.employee)
        return self.queryset.none()


class MissionViewSet(viewsets.ModelViewSet):
    swagger_tags = ['missions']
    permission_classes = [IsAuthenticated]
    serializer_class = MissionSerializer
    queryset = Mission.objects.all()

    def get_permissions(self):
        perms_map = {
            'list': [IsAuthenticated(), IsViewMissionPermission()],
            'create': [IsAuthenticated(), IsAddMissionPermission()],
            'update': [IsAuthenticated(), IsModifyMissionPermission()],
            'partial_update': [IsAuthenticated(), IsModifyMissionPermission()],
            'destroy': [IsAuthenticated(), IsDeleteMissionPermission()],
        }
        return perms_map.get(self.action, [IsAuthenticated()])