
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from tripsservice.models.TransportModel import Transport
from tripsservice.views.TransportPermission import IsViewAllTransportPermission
from tripsservice.serializers.TransportSerializer import TransportSerializer


class TransportView(APIView):
    
    permission_classes = [IsAuthenticated, IsViewAllTransportPermission]

    def get(self, request):
        transports = Transport.objects.all()
        return Response({
            "transports": TransportSerializer(transports, many=True).data,
        })