from rest_framework import serializers
from .models import TransportationModes, Trips, Missions


class TransportationModesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportationModes
        fields = ['transportation']


class MissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Missions
        fields = ['start_date', 'end_date', 'mission_reason']


class TripsSerializer(serializers.ModelSerializer):
    transportation = TransportationModesSerializer()
    mission = MissionsSerializer()

    class Meta:
        model = Trips
        fields = [
            'trip_id', 'trip_date', 'departure_city', 'departure_country',
            'destination_city', 'destination_country', 'trip_reason',
            'is_round_trip', 'carpooling', 'carbon_footprint', 
            'mission', 'transportation'
        ]
