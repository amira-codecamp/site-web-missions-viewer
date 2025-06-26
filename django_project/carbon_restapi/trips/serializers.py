from rest_framework import serializers
from carbon_restapi.trips.models import Employee, Status, Trip, Mission, Transport
import re
from unidecode import unidecode


class StatusSerializer(serializers.ModelSerializer):
    """
    Serializer for Status model.
    """
    class Meta:
        model = Status
        fields = ['status_name']
        extra_kwargs = {
            'status_name': {'validators': []},  # Disable unique validator
        }


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for Employee model.
    """
    status = StatusSerializer()  # Nested serializer for status

    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'email', 'status']
        extra_kwargs = {
            'email': {'validators': []},  # Disable unique validator
        }
        read_only_fields = ['employee_id']

    def validate_email(self, value):
        """
        Validate that email belongs to allowed LIPN domains.
        """
        allowed_domains = [r'^[^@]+@lipn\.fr$', r'^[^@]+@lipn\.univ-paris13\.fr$']
        if not any(re.match(pattern, value) for pattern in allowed_domains):
            raise serializers.ValidationError("Invalid email address. Only members of LIPN are allowed!")
        return value

    def update(self, instance, validated_data):
        """
        Update Employee instance.
        """
        status_data = validated_data.pop('status', None)
        if status_data:
            # Assign existing Status instance based on status_name
            instance.status = Status.objects.get(status_name=status_data['status_name'])

        # Update other fields on Employee
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class TransportSerializer(serializers.ModelSerializer):
    """
    Serializer for Transport model.
    """
    class Meta:
        model = Transport
        fields = ['transport_name']
        extra_kwargs = {
            'transport_name': {'validators': []},  # Disable unique validator
        }


class MissionSerializer(serializers.ModelSerializer):
    """
    Serializer for Mission model.
    """
    employee = EmployeeSerializer()

    class Meta:
        model = Mission
        fields = ['mission_id', 'start_date', 'end_date', 'mission_desc', 'employee']
        extra_kwargs = {
            'mission_desc': {'validators': []},  # Disable unique validator
        }
        read_only_fields = ['mission_id']

    def create(self, validated_data):
        """
        Create Mission instance.
        """
        employee_data = validated_data.pop('employee')
        employee = Employee.objects.get(email=employee_data['email'])
        mission = Mission.objects.create(employee=employee, **validated_data)
        return mission

    def update(self, instance, validated_data):
        """
        Update Mission instance.
        """
        employee_data = validated_data.pop('employee', None)
        if employee_data:
            instance.employee = Employee.objects.get(email=employee_data['email'])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


class TripSerializer(serializers.ModelSerializer):
    """
    Serializer for Trip model.
    """
    transport = TransportSerializer()
    mission = MissionSerializer()

    class Meta:
        model = Trip
        fields = [
            'trip_id',
            'departure_city', 'departure_country',
            'destination_city', 'destination_country',
            'is_round_trip', 'carpooling', 'carbon_footprint',
            'transport', 'mission'
        ]
        read_only_fields = ['trip_id', 'carbon_footprint']

    def create(self, validated_data):
        """
        Create Trip instance.
        """
        transport_data = validated_data.pop('transport')
        mission_data = validated_data.pop('mission')

        transport = Transport.objects.get(transport_name=transport_data['transport_name'])
        mission = Mission.objects.get(mission_desc=mission_data['mission_desc'])

        trip = Trip.objects.create(transport=transport, mission=mission, **validated_data)
        trip.save()
        return trip

    def update(self, instance, validated_data):
        """
        Update Trip instance.
        """
        transport_data = validated_data.pop('transport', None)
        mission_data = validated_data.pop('mission', None)

        if transport_data:
            instance.transport = Transport.objects.get(transport_name=transport_data['transport_name'])
        if mission_data:
            instance.mission = Mission.objects.get(mission_desc=mission_data['mission_desc'])

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance