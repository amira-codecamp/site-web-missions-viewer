
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from tripsservice.models.TripModel import Trip
from tripsservice.views.TripPermission import IsViewTripPermission
from tripsservice.serializers.TripSerializer import TripSerializer


class TripView(APIView):
    
    permission_classes = [IsAuthenticated, IsViewTripPermission]

    def get(self, request):
        if request.user.group.group_name == 'admin':
            trips = Trip.objects.all()
        else:
            trips = Trip.objects.filter(employee_id=request.user.employee_id)
        if not trips:
            raise NotFound(detail="Trips not found.")
        return Response({
            "trips": TripSerializer(trips, many=True).data,
        })