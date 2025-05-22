
from rest_framework import serializers


class TravelSerializer(serializers.Serializer):
    transport = serializers.CharField()
    departure_country = serializers.CharField()
    destination_country = serializers.CharField()
    departure_lat = serializers.FloatField()
    departure_long = serializers.FloatField()
    destination_lat = serializers.FloatField()
    destination_long = serializers.FloatField()
    year = serializers.CharField()
    carpooling = serializers.IntegerField(default=1)
    is_round_trip = serializers.BooleanField(default=False)