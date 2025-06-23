from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from trips.models import Employee, Status, Trip, Mission, Transport

from trips.serializers import (
    TripSerializer,
    MissionSerializer,
    EmployeeSerializer, 
    StatusSerializer,
    TransportSerializer
)

from trips.permissions import (
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


# View to retrieve status list
class StatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employeesstatus = Status.objects.all()
        serializer = StatusSerializer(employeesstatus, many=True)
        return Response({"status": serializer.data}, status=status.HTTP_200_OK)


# View for employees table
class EmployeeView(APIView):
    permission_classes = [IsAuthenticated, IsViewEmployeePermission]

    def get(self, request): # get to retrieve employee list
        employees = Employee.objects.select_related('status').all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response({"employees": serializer.data}, status=status.HTTP_200_OK)
    
    # PUT : Update an Employee
    def put(self, request):
        # Permission check
        if not IsModifyEmployeePermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        employee_id = request.data.get('employee_id')
        if not employee_id:
            return Response({'error': 'Employee ID is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Get employee instance
            employee = Employee.objects.get(employee_id=employee_id)
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Use partial=True for partial update
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    

# View to retrieve transport modes
class TransportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transports = Transport.objects.all()
        serializer = TransportSerializer(transports, many=True)
        return Response({"transports": serializer.data}, status=status.HTTP_200_OK)


# View for CRUD operations on Trip
class TripView(APIView):
    permission_classes = [IsAuthenticated]

    # GET: Return all trips or only user's trips
    def get(self, request):
        if IsViewTripPermission().has_permission(request, self):
            if request.user.group.group_name == 'missionmanager':
                trips = Trip.objects.select_related('mission', 'transport').all()
            else:
                trips = Trip.objects.select_related('mission', 'transport').filter(
                     mission__employee=request.user.employee
                )
            return Response({
                "trips": TripSerializer(trips, many=True).data,
            })
        else:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    # POST: Create a new trip
    def post(self, request):
        if not IsAddTripPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = TripSerializer(data=request.data)

        if serializer.is_valid():
            try:
                trip = serializer.save()
                return Response(TripSerializer(trip).data, status=status.HTTP_201_CREATED)
            except (Transport.DoesNotExist, Mission.DoesNotExist) as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # PUT: Update a trip
    def put(self, request):
        # Permission check
        if not IsModifyTripPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        trip_id = request.data.get('trip_id')
        if not trip_id:
            return Response({'error': 'trip_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try: # Get trip row
            trip = Trip.objects.get(trip_id=trip_id)
        except Trip.DoesNotExist:
            return Response({'error': 'Trip not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Pass request.data with partial=True for partial update
        serializer = TripSerializer(trip, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # <-- calls custom update method internally

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Delete an existing trip
    def delete(self, request):
        if not IsDeleteTripPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        trip_id = request.data.get('trip_id')
        if not trip_id:
            return Response({'error': 'trip_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            trip = Trip.objects.get(trip_id=trip_id)
            trip.delete()
            return Response({'message': 'Trip deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Trip.DoesNotExist:
            return Response({'error': 'Trip not found.'}, status=status.HTTP_404_NOT_FOUND)


# View to handle missions
class MissionView(APIView):
    permission_classes = [IsAuthenticated]

    # GET: List all missions
    def get(self, request):
        if not IsViewMissionPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        missions = Mission.objects.all()
        return Response({"missions": MissionSerializer(missions, many=True).data})

    # POST: Create a new mission
    def post(self, request):
        if not IsAddMissionPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = MissionSerializer(data=request.data)

        if serializer.is_valid():
            try:
                mission = serializer.save()
                return Response(MissionSerializer(mission).data, status=status.HTTP_201_CREATED)
            except (Employee.DoesNotExist) as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete an existing mission
    def delete(self, request):
        if not IsDeleteMissionPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        mission_id = request.data.get('mission_id')
        if not mission_id:
            return Response({'error': 'mission_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            mission = Mission.objects.get(mission_id=mission_id)
            mission.delete()
            return Response({'message': 'Mission deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Mission.DoesNotExist:
            return Response({'error': 'Mission not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    # PUT: Update a mission
    def put(self, request):
        # Permission check
        if not IsModifyMissionPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        mission_id = request.data.get('mission_id')
        if not mission_id:
            return Response({'error': 'mission_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try: # Get mission row
            mission = Mission.objects.get(mission_id=mission_id)
        except Mission.DoesNotExist:
            return Response({'error': 'Mission not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Pass request.data with partial=True for partial update
        serializer = MissionSerializer(mission, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # <-- calls custom update method internally

        return Response(serializer.data, status=status.HTTP_200_OK)
