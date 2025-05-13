
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from tripsservice.models.TripModel import Trip
from tripsservice.views.TripPermission import IsViewTripPermission, IsViewAllTripPermission
from tripsservice.serializers.TripSerializer import TripSerializer


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