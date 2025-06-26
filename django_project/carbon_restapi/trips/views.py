from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from carbon_restapi.trips.models import Employee, Status, Trip, Mission, Transport
from carbon_restapi.trips.serializers import (
    TripSerializer,
    MissionSerializer,
    EmployeeSerializer,
    StatusSerializer,
    TransportSerializer
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
    IsModifyEmployeePermission
)


class StatusViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StatusSerializer

    def list(self, request):
        """GET: Return list of all status."""
        statuses = Status.objects.all()
        serializer = self.serializer_class(statuses, many=True)
        return Response({"status": serializer.data}, status=status.HTTP_200_OK)


class EmployeeViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSerializer

    def list(self, request):
        """GET: Return list of employees."""
        if not IsViewEmployeePermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        employees = Employee.objects.select_related('status').all()
        serializer = self.serializer_class(employees, many=True)
        return Response({"employees": serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        """PUT: Update an existing employee."""
        if not IsModifyEmployeePermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        if not pk:
            return Response({'error': 'Employee ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee = Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(employee, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TransportViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TransportSerializer

    def list(self, request):
        """GET: Return all transport modes."""
        transports = Transport.objects.all()
        serializer = self.serializer_class(transports, many=True)
        return Response({"transports": serializer.data}, status=status.HTTP_200_OK)


class TripViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TripSerializer

    def list(self, request):
        """GET: Return trips; all if manager, else user's trips."""
        if not IsViewTripPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        if request.user.group.group_name == 'MISSIONMANAGER':
            trips = Trip.objects.select_related('mission', 'transport').all()
        else:
            trips = Trip.objects.select_related('mission', 'transport').filter(mission__employee=request.user.employee)

        serializer = self.serializer_class(trips, many=True)
        return Response({"trips": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request):
        """POST: Create a new trip."""
        if not IsAddTripPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                trip = serializer.save()
                return Response(self.serializer_class(trip).data, status=status.HTTP_201_CREATED)
            except (Transport.DoesNotExist, Mission.DoesNotExist) as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """PUT: Update an existing trip."""
        if not IsModifyTripPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        if not pk:
            return Response({'error': 'trip_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            trip = Trip.objects.get(pk=pk)
        except Trip.DoesNotExist:
            return Response({'error': 'Trip not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(trip, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """DELETE: Remove a trip."""
        if not IsDeleteTripPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        if not pk:
            return Response({'error': 'trip_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            trip = Trip.objects.get(pk=pk)
            trip.delete()
            return Response({'message': 'Trip deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Trip.DoesNotExist:
            return Response({'error': 'Trip not found.'}, status=status.HTTP_404_NOT_FOUND)


class MissionViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = MissionSerializer

    def list(self, request):
        """GET: Return list of missions."""
        if not IsViewMissionPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        missions = Mission.objects.all()
        serializer = self.serializer_class(missions, many=True)
        return Response({"missions": serializer.data})

    def create(self, request):
        """POST: Create a new mission."""
        if not IsAddMissionPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                mission = serializer.save()
                return Response(self.serializer_class(mission).data, status=status.HTTP_201_CREATED)
            except Employee.DoesNotExist as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """PUT: Update an existing mission."""
        if not IsModifyMissionPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        if not pk:
            return Response({'error': 'mission_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            mission = Mission.objects.get(pk=pk)
        except Mission.DoesNotExist:
            return Response({'error': 'Mission not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(mission, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """DELETE: Delete mission with primary key."""
        if not IsDeleteMissionPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        if not pk:
            return Response({'error': 'mission_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            mission = Mission.objects.get(pk=pk)
            mission.delete()
            return Response({'message': 'Mission deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Mission.DoesNotExist:
            return Response({'error': 'Mission not found.'}, status=status.HTTP_404_NOT_FOUND)