from rest_framework import serializers
from users.UserModel import User, Group
from trips.serializers import EmployeeSerializer
from trips.models import Employee


class GroupSerializer(serializers.ModelSerializer):
    # Serialize Group model
    class Meta:
        model = Group
        fields = ['group_name']
        extra_kwargs = {
            'group_name': {'validators': []},
        }


class UserSerializer(serializers.ModelSerializer):
    group = GroupSerializer() # Nested serialization of group
    employee = EmployeeSerializer()  # Nested serialization of employee
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['login', 'password', 'date_joined', 'last_login', 'is_active', 'group', 'employee']

    def create(self, validated_data):
        # Nested data from the payload
        password = validated_data.pop('password')
        employee_data = validated_data.pop('employee')
        group_data = validated_data.pop('group')

        # Retrieve Employee instance
        employee = Employee.objects.get(email=employee_data['email'])

        # Retrieve Group instance
        group = Group.objects.get(group_name=group_data['group_name'])

        # Create the User
        user = User.objects.create(
            employee=employee,
            group=group,
            **validated_data
        )

        user.set_password(password)  # hash the password before saving
        user.save()

        return user