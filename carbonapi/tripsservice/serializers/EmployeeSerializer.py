
from rest_framework import serializers
from tripsservice.models.EmployeeModel import Employee, EmployeeStatus


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeStatus
        fields = ['status_name']


class EmployeeWithStatusSerializer(serializers.ModelSerializer):

    status = StatusSerializer()

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'status']


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email']