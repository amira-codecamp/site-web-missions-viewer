from rest_framework import serializers
from users.UserModel import User, Group
from trips.serializers import EmployeeSerializer


class GroupSerializer(serializers.ModelSerializer):
    # Serialize Group model
    class Meta:
        model = Group
        fields = ['group_name']


class UserSerializer(serializers.ModelSerializer):
    group = GroupSerializer()
    employee = EmployeeSerializer()  # Nested serialization of employee

    class Meta:
        model = User
        fields = ['login', 'date_joined', 'last_login', 'is_active', 'group', 'employee']