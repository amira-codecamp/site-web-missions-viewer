
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from emissionsservice.models.TravelEmission import TravelEmission
from emissionsservice.serializers.TravelSerializer import TravelSerializer


class TravelEmissionView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TravelSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            data = serializer.validated_data

            carbon = TravelEmission.carbon_footprint(
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
