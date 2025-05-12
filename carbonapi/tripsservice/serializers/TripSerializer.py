
from rest_framework import serializers
from tripsservice.serializers.EmployeeSerializer import EmployeeSerializer
from tripsservice.serializers.TransportSerializer import TransportSerializer
from tripsservice.models.TripModel import Trip, Mission


class MissionsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Mission
        fields = ['start_date', 'end_date', 'mission_desc']


class TripSerializer(serializers.ModelSerializer):

    transport = TransportSerializer()
    mission = MissionsSerializer()
    employee = EmployeeSerializer()

    class Meta:
        model = Trip
        fields = [
            'trip_id', 'departure_city', 'departure_country',
            'destination_city', 'destination_country', 
            'is_round_trip', 'carpooling', 'carbon_footprint', 
            'transport', 'mission', 'employee'
        ]
