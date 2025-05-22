
from rest_framework import serializers
from tripsservice.serializers.EmployeeSerializer import EmployeeSerializer, EmployeeWithStatusSerializer
from tripsservice.serializers.TransportSerializer import TransportSerializer
from tripsservice.models.TripModel import Trip, Mission
from tripsservice.models.TransportModel import Transport


class MissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Mission
        fields = ['mission_num', 'start_date', 'end_date', 'mission_desc']


class TripSerializer(serializers.ModelSerializer):

    transport = TransportSerializer()
    mission = MissionSerializer()
    employee = EmployeeWithStatusSerializer()

    class Meta:
        model = Trip
        fields = [
            'trip_id', 'departure_city', 'departure_country',
            'destination_city', 'destination_country', 
            'is_round_trip', 'carpooling', 'carbon_footprint', 
            'transport', 'mission', 'employee'
        ]


class TripCreateSerializer(serializers.ModelSerializer):
    transport_name = serializers.PrimaryKeyRelatedField(queryset=Transport.objects.all())
    mission_num = serializers.PrimaryKeyRelatedField(queryset=Mission.objects.all())
    employee = EmployeeSerializer()

    class Meta:
        model = Trip
        fields = [
            'departure_city', 'departure_country',
            'destination_city', 'destination_country', 
            'is_round_trip', 'carpooling',
            'is_round_trip', 'carpooling', 'carbon_footprint',
            'transport_name', 'mission_num', 'employee'
        ]