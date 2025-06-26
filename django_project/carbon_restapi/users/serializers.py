from rest_framework import serializers
from carbon_restapi.users.models import User, Group
from carbon_restapi.trips.serializers import EmployeeSerializer
from carbon_restapi.trips.models import Employee
from unidecode import unidecode


class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for Group model.
    """
    class Meta:
        model = Group
        fields = ['group_name']
        extra_kwargs = {
            'group_name': {'validators': []},  # Disable unique validator
        }


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    group = GroupSerializer()
    employee = EmployeeSerializer()
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['user_id', 'login', 'password', 'date_joined', 'last_login', 'is_active', 'group', 'employee']
        read_only_fields = ['user_id']

    def validate(self, attrs):
        """
        Presence of nested 'group' and 'employee'.
        """
        if 'group' not in attrs:
            raise serializers.ValidationError({"group": "Group data is required."})
        if 'employee' not in attrs:
            raise serializers.ValidationError({"employee": "Employee data is required."})
        return attrs

    def create(self, validated_data):
        """
        Create a new User instance.
        """
        password = validated_data.pop('password', None)
        employee_data = validated_data.pop('employee')
        group_data = validated_data.pop('group')

        try:
            employee = Employee.objects.get(email=employee_data['email'])
        except Employee.DoesNotExist:
            raise serializers.ValidationError({"employee": "Employee with this email does not exist."})

        try:
            group = Group.objects.get(group_name=group_data['group_name'])
        except Group.DoesNotExist:
            raise serializers.ValidationError({"group": "Group with this name does not exist."})

        user = User.objects.create(
            employee=employee,
            group=group,
            **validated_data
        )

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()  # In case password is not provided

        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update existing User instance.
        """
        employee_data = validated_data.pop('employee', None)
        group_data = validated_data.pop('group', None)
        password = validated_data.pop('password', None)

        if employee_data:
            try:
                employee = Employee.objects.get(email=employee_data['email'])
                instance.employee = employee
            except Employee.DoesNotExist:
                raise serializers.ValidationError({"employee": "Employee with this email does not exist."})

        if group_data:
            try:
                group = Group.objects.get(group_name=group_data['group_name'])
                instance.group = group
            except Group.DoesNotExist:
                raise serializers.ValidationError({"group": "Group with this name does not exist."})

        # Update remaining user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Update password only if provided
        if password and password != '*****':
            instance.set_password(password)

        instance.save()
        return instance