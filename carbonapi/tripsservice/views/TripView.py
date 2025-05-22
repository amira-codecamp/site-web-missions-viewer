
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from tripsservice.models.TripModel import Trip, Mission
from tripsservice.models.EmployeeModel import Employee
from tripsservice.views.TripPermission import IsViewTripPermission, IsViewAllTripPermission, IsAddTripPermission, IsViewAllMissionPermission
from tripsservice.serializers.TripSerializer import TripSerializer, TripCreateSerializer, MissionSerializer


class TripView(APIView):
    
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if IsViewAllTripPermission().has_permission(request, self):
            trips = Trip.objects.all()
        elif IsViewTripPermission().has_permission(request, self):
            trips = Trip.objects.filter(employee_id=request.user.employee_id)
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
                trip = Trip.objects.create(
                    employee=Employee.objects.get(
                        email=employee['email']
                    ),
                    mission=mission_num,
                    transport=transport_name,
                    carbon_footprint=carbon_footprint,
                    **validated_data
                )
                return Response(TripSerializer(trip).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)


class MissionView(APIView):
    
    permission_classes = [IsAuthenticated, IsViewAllMissionPermission]

    def get(self, request):
        missions = Mission.objects.all()
        return Response({
            "missions": MissionSerializer(missions, many=True).data,
        })
    
    # def post(self, request):