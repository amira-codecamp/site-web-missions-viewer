from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from carbon.Travel import Travel
from carbon.Serializer import InputSerializer


class CarbonView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def post(self, request):
        serializer = InputSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            # Calculate carbon footprint from travel data
            carbon = Travel.carbon_footprint(
                transport=data['transport'],
                departure_country=data['departure_country'],
                destination_country=data['destination_country'],
                departure_lat=data['departure_lat'],
                departure_long=data['departure_long'],
                destination_lat=data['destination_lat'],
                destination_long=data['destination_long'],
                carpooling=data.get('carpooling'),
                is_round_trip=data.get('is_round_trip'),
                year=data.get('year'),
            )

            if carbon is None:
                return Response({"error": "Could not compute carbon footprint."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"carbon_footprint": carbon}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)