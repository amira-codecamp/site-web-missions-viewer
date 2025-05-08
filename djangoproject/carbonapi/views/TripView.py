
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from carbonapi.models.TripModel import Trip
from carbonapi.views.TripPermission import IsViewTripPermission
from carbonapi.serializers.TripSerializer import TripSerializer


class TripView(APIView):
    
    permission_classes = [IsAuthenticated, IsViewTripPermission]

    def get(self, request):
        trips = Trip.objects.filter(employee_id=request.user.employee_id)
        if not trips:
            raise NotFound(detail="Trips not found.")
        return Response({
            "trips": TripSerializer(trips, many=True).data,
        })