
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from tripsservice.models.TripModel import Trip, Mission
from tripsservice.models.EmployeeModel import Employee

from tripsservice.views.TripPermission import (
    IsViewTripPermission,
    IsViewAllTripPermission,
    IsAddTripPermission,
    IsViewAllMissionPermission,
    IsAddMissionPermission,
    IsDeleteTripPermission,
    IsModifyTripPermission,
)

from tripsservice.serializers.TripSerializer import (
    TripSerializer,
    TripCreateSerializer,
    TripAlterSerializer,
    TripIdSerializer,
    MissionSerializer,
)


class TripView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if IsViewAllTripPermission().has_permission(request, self):
            trips = Trip.objects.all()
        elif IsViewTripPermission().has_permission(request, self):
            trips = Trip.objects.filter(employee_id=request.user.employee_id)
        else:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        return Response({
            "trips": TripSerializer(trips, many=True).data,
        })

    def post(self, request):
        if IsAddTripPermission().has_permission(request, self):
            serializer = TripCreateSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                employee = validated_data.pop('employee')
                mission_num = validated_data.pop('mission_num')
                transport_name = validated_data.pop('transport_name')
                carbon_footprint = validated_data.pop('carbon_footprint')
                try:
                    employee_obj = Employee.objects.get(email=employee['email'])
                except Employee.DoesNotExist:
                    return Response({'error': 'Employee not found.'}, status=status.HTTP_400_BAD_REQUEST)
                trip = Trip.objects.create(
                    employee=employee_obj,
                    mission=mission_num,
                    transport=transport_name,
                    carbon_footprint=carbon_footprint,
                    **validated_data
                )
                return Response(TripSerializer(trip).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        if IsDeleteTripPermission().has_permission(request, self):
            serializer = TripIdSerializer(data=request.data)
            if serializer.is_valid():
                trip_id = serializer.validated_data['trip_id']
                try:
                    trip = Trip.objects.get(trip_id=trip_id)
                    trip.delete()
                    return Response({'message': 'Trip deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
                except Trip.DoesNotExist:
                    return Response({'error': 'Trip not found.'}, status=status.HTTP_404_NOT_FOUND)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
    def put(self, request):
        if not IsModifyTripPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        trip_id = request.data.get('trip_id')
        try:
            trip = Trip.objects.get(trip_id=trip_id)
        except Trip.DoesNotExist:
            return Response({'detail': 'Trip not found.'}, status=status.HTTP_404_NOT_FOUND)
        employee_data = request.data.get('employee')
        try:
            employee_obj = Employee.objects.get(email=employee_data['email'])
        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found.'}, status=status.HTTP_400_BAD_REQUEST)
        request.data['employee'] = employee_obj.employee_id
        request.data['mission'] = request.data.pop('mission_num')
        request.data['transport'] = request.data.pop('transport_name')
        serializer = TripAlterSerializer(trip, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class MissionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if IsViewAllMissionPermission().has_permission(request, self):
            missions = Mission.objects.all()
        else:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        return Response({
            "missions": MissionSerializer(missions, many=True).data,
        })
    
    def post(self, request):
        if IsAddMissionPermission().has_permission(request, self):
            serializer = MissionSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data
                mission = Mission.objects.create(
                    **validated_data
                )
                return Response(MissionSerializer(mission).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)