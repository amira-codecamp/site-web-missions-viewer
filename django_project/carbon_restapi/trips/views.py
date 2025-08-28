from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import action

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
    IsAddEmployeePermission
)

from carbon_restapi.trips.filters import TripFilter, MissionFilter, EmployeeFilter


class StatusViewSet(viewsets.ReadOnlyModelViewSet):
    swagger_tags = ['status']
    http_method_names = ['get', 'head', 'options']
    permission_classes = [IsAuthenticated]
    serializer_class = StatusSerializer
    queryset = Status.objects.all()


class EmployeeViewSet(viewsets.ModelViewSet):
    swagger_tags = ['employees']
    http_method_names = ['get', 'put', 'patch', 'head', 'options', 'post']
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer
    queryset = Employee.objects.select_related('status').all()
    filterset_class = EmployeeFilter

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated(), IsViewEmployeePermission()]
        if self.action in ('update', 'partial_update'):
            return [IsAuthenticated(), IsModifyEmployeePermission()]
        if self.action == 'create':
            return [IsAuthenticated(), IsAddEmployeePermission()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user.employee)
        return Response(serializer.data)


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
    ordering = ['mission__employee__last_name', '-mission__start_date']  # descending order

    def get_permissions(self):
        perms_map = {
            'list': [IsAuthenticated(), IsViewTripPermission()],
            'retrieve': [IsAuthenticated(), IsViewTripPermission()],
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
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = MissionFilter
    ordering = ['employee__last_name', '-start_date']  # descending order

    def get_permissions(self):
        perms_map = {
            'list': [IsAuthenticated(), IsViewMissionPermission()],
            'retrieve': [IsAuthenticated(), IsViewMissionPermission()],
            'create': [IsAuthenticated(), IsAddMissionPermission()],
            'update': [IsAuthenticated(), IsModifyMissionPermission()],
            'partial_update': [IsAuthenticated(), IsModifyMissionPermission()],
            'destroy': [IsAuthenticated(), IsDeleteMissionPermission()],
        }
        return perms_map.get(self.action, [IsAuthenticated()])
    
    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'group') and user.group.group_name == 'MISSIONMANAGER':
            return self.queryset
        if hasattr(user, 'employee'):
            return self.queryset.filter(employee=user.employee)
        return self.queryset.none()