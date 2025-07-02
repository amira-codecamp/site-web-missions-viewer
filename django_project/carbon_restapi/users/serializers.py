from rest_framework import serializers
from carbon_restapi.users.models import User, Group
from carbon_restapi.trips.models import Employee


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['group_name']


class UserSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(
        queryset=Group.objects.all()
    )
    employee = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all()
    )
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            'user_id', 'login', 'password', 'date_joined', 'last_login', 'is_active',
            'group', 'employee'
        ]
        read_only_fields = ['user_id', 'date_joined', 'last_login']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance