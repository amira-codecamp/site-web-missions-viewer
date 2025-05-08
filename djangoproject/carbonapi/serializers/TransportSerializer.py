
from rest_framework import serializers
from carbonapi.models.TransportModel import Transport


class TransportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transport
        fields = ['transport_name']