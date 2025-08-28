from rest_framework import serializers
from carbon_restapi.trips.models import Employee, Status, Trip, Mission, Transport
import re
import bleach
from datetime import date


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['status_name']


class EmployeeSerializer(serializers.ModelSerializer):
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())

    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'email', 'status', 'research_team', 'employee_adm_num']
        read_only_fields = ['employee_id']

    def validate_email(self, value):
        cleaned = bleach.clean(value.strip(), tags=[], strip=True)
        return cleaned


class TransportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transport
        fields = ['transport_name']


class MissionSerializer(serializers.ModelSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = Mission
        fields = ['mission_id', 'start_date', 'end_date', 'mission_adm_num', 'mission_desc', 'employee']
        read_only_fields = ['mission_id']

    def validate_start_date(self, value):
        if value is None:
            raise serializers.ValidationError("start_date cannot be null.")
        if value > date.today():
            raise serializers.ValidationError("start_date cannot be in the future.")
        return value

    def validate_end_date(self, value):
        if value is None:
            raise serializers.ValidationError("end_date cannot be null.")
        if value > date.today():
            raise serializers.ValidationError("end_date cannot be in the future.")
        return value

    def validate_mission_desc(self, value):
        clean_value = bleach.clean(value.strip(), tags=[], strip=True)
        return clean_value

    def validate_mission_adm_num(self, value):
        clean_value = bleach.clean(value.strip(), tags=[], strip=True)
        return clean_value

    def validate(self, attrs):
        start = attrs.get('start_date')
        end = attrs.get('end_date')
        if end < start:
            raise serializers.ValidationError("end_date must be greater than or equal to start_date.")
        return attrs


class TripSerializer(serializers.ModelSerializer):
    mission = serializers.PrimaryKeyRelatedField(queryset=Mission.objects.all())
    transport = serializers.PrimaryKeyRelatedField(queryset=Transport.objects.all())

    class Meta:
        model = Trip
        fields = [
            'trip_id',
            'departure_city', 'departure_country',
            'destination_city', 'destination_country',
            'is_round_trip', 'carpooling', 'carbon_footprint',
            'transport', 'mission',
        ]
        read_only_fields = ['trip_id', 'carbon_footprint']

    def validate_departure_city(self, value):
        cleaned = bleach.clean(value.strip(), tags=[], strip=True)
        if not cleaned:
            raise serializers.ValidationError("departure_city cannot be empty or invalid.")
        return cleaned

    def validate_departure_country(self, value):
        cleaned = bleach.clean(value.strip(), tags=[], strip=True)
        if not cleaned:
            raise serializers.ValidationError("departure_country cannot be empty or invalid.")
        return cleaned

    def validate_destination_city(self, value):
        cleaned = bleach.clean(value.strip(), tags=[], strip=True)
        if not cleaned:
            raise serializers.ValidationError("destination_city cannot be empty or invalid.")
        return cleaned

    def validate_destination_country(self, value):
        cleaned = bleach.clean(value.strip(), tags=[], strip=True)
        if not cleaned:
            raise serializers.ValidationError("destination_country cannot be empty or invalid.")
        return cleaned

    def validate_carpooling(self, value):
        if value < 1:
            raise serializers.ValidationError("carpooling must be greater than or equal to 1.")
        return value