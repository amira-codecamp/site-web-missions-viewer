from rest_framework import serializers
from api.models import TransportationModes, Trips, Missions, Employees, StaffStatus


class TransportationModesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransportationModes
        fields = ['transportation_name']


class MissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Missions
        fields = ['start_date', 'end_date', 'mission_reason']


class StaffStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffStatus
        fields = ['status_name']


class EmployeesSerializer(serializers.ModelSerializer):
    status = StaffStatusSerializer()

    class Meta:
        model = Employees
        fields = ['first_name', 'last_name', 'email', 'status']


class TripsSerializer(serializers.ModelSerializer):
    transportation = TransportationModesSerializer()
    mission = MissionsSerializer()
    employee = EmployeesSerializer()

    class Meta:
        model = Trips
        fields = [
            'trip_id', 'trip_date', 'departure_city', 'departure_country',
            'destination_city', 'destination_country', 'trip_reason',
            'is_round_trip', 'carpooling', 'carbon_footprint', 
            'mission', 'transportation', 'employee'
        ]
