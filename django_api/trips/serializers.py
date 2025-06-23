from rest_framework import serializers
from trips.models import Employee, Status, Trip, Mission, Transport
import re


# Serializer for the Status model
class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ['status_name']
        extra_kwargs = {
            'status_name': {'validators': []},
        }


# Serializer for the Employee model
class EmployeeSerializer(serializers.ModelSerializer):

    status = StatusSerializer() # nested status

    class Meta:
        model = Employee
        fields = ['employee_id', 'first_name', 'last_name', 'email', 'status']
        extra_kwargs = {
            'email': {'validators': []},
        }
        read_only_fields = ['employee_id']

    def validate_email(self, value):
        if not re.match(r'^[^@]+@lipn\.fr$', value) and not re.match(r'^[^@]+@lipn\.univ-paris13\.fr$', value):
            raise serializers.ValidationError("Invalid email address. Only members of LIPN are allowed!")
        return value

    def update(self, instance, validated_data):
        # Nested data from the payload
        status_data = validated_data.pop('status')

        # Retrieve status instance
        instance.status = Status.objects.get(status_name=status_data['status_name'])

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# Serializer for the Transport model
class TransportSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transport
        fields = ['transport_name']
        extra_kwargs = {
            'transport_name': {'validators': []},
        }


# Serializer for the Mission model
class MissionSerializer(serializers.ModelSerializer):

    employee = EmployeeSerializer() # nested employee
    
    class Meta:
        model = Mission
        fields = ['mission_id', 'start_date', 'end_date', 'mission_desc', 'employee']
        extra_kwargs = {
            'mission_desc': {'validators': []},
        }
        read_only_fields = ['mission_id']

    def create(self, validated_data):
        # Nested data from the payload
        employee_data = validated_data.pop('employee')

        # Retrieve Transport instance
        employee = Employee.objects.get(email=employee_data['email'])

        # Create the Mission
        mission = Mission.objects.create(
            employee=employee,
            **validated_data
        )

        return mission

    def update(self, instance, validated_data):
        # Nested data from the payload
        employee_data = validated_data.pop('employee')

        # Retrieve Employee instance
        instance.employee = Employee.objects.get(email=employee_data['email'])

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# Serializer for the Trip model
class TripSerializer(serializers.ModelSerializer):

    transport = TransportSerializer() # nested transport
    mission = MissionSerializer() # nested mission

    class Meta:
        model = Trip
        fields = [
            'trip_id',
            'departure_city', 'departure_country',
            'destination_city', 'destination_country', 
            'is_round_trip', 'carpooling', 'carbon_footprint', 
            'transport', 'mission'
        ]
        read_only_fields = ['trip_id']

    def create(self, validated_data):
        # Nested data from the payload
        transport_data = validated_data.pop('transport')
        mission_data = validated_data.pop('mission')

        # Retrieve Transport instance
        transport = Transport.objects.get(transport_name=transport_data['transport_name'])

        # Retrieve Mission instance
        mission = Mission.objects.get(mission_desc=mission_data['mission_desc'])

        # Create the Trip
        trip = Trip.objects.create(
            transport=transport,
            mission=mission,
            **validated_data
        )

        return trip

    def update(self, instance, validated_data):
        # Nested data from the payload
        transport_data = validated_data.pop('transport')
        mission_data = validated_data.pop('mission')

        # Retrieve Transport instance
        instance.transport = Transport.objects.get(transport_name=transport_data['transport_name'])

        # Retrieve Mission instance
        instance.mission = Mission.objects.get(mission_desc=mission_data['mission_desc'])

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance