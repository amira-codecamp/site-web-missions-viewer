from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from api.models import Trips
from api.serializers import TripsSerializer


class TripsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        trips = Trips.objects.filter(employee_id=request.user.employee_id)

        if not trips:
            raise NotFound(detail="Trips not found.")

        return Response({
            "trips": TripsSerializer(trips, many=True).data,
        })
    

class HomeView(APIView):

    def get(self, request):
        return Response({
            "data": "WELCOME HOME PAGE ! LIPN GENERAL STATS",
        })