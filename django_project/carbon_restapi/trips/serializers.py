from rest_framework import serializers
from carbon_restapi.trips.models import Employee, Status, Trip, Mission, Transport
import re


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['status_name']


class EmployeeSerializer(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(
        queryset=Status.objects.all()
    )

    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'email', 'status']
        read_only_fields = ['employee_id']

    def validate_email(self, value):
        allowed_domains = [r'^[^@]+@lipn\.fr$', r'^[^@]+@lipn\.univ-paris13\.fr$']
        if not any(re.match(pattern, value) for pattern in allowed_domains):
            raise serializers.ValidationError(
                "Invalid email address: Only LIPN members are allowed."
            )
        return value


class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = ['transport_name']


class MissionSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(read_only=True)

    class Meta:
        model = Mission
        fields = ['mission_id', 'start_date', 'end_date', 'mission_desc', 'employee']
        read_only_fields = ['mission_id']


class TripSerializer(serializers.ModelSerializer):
    transport = serializers.PrimaryKeyRelatedField(
        queryset=Transport.objects.all()
    )
    mission = MissionSerializer(read_only=True)
    mission_id = serializers.PrimaryKeyRelatedField(
        queryset=Mission.objects.all(),
        source='mission',
        write_only=True
    )

    class Meta:
        model = Trip
        fields = [
            'trip_id',
            'departure_city', 'departure_country',
            'destination_city', 'destination_country',
            'is_round_trip', 'carpooling', 'carbon_footprint',
            'transport',
            'mission',
            'mission_id',
        ]
        read_only_fields = ['trip_id', 'carbon_footprint']