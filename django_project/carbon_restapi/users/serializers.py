from rest_framework import serializers
from carbon_restapi.users.models import User, Group
from carbon_restapi.trips.models import Employee
from rest_framework_simplejwt.tokens import AccessToken, UntypedToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
import bleach
import re


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['group_name']


class UserSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())

    class Meta:
        model = User
        fields = [
            'user_id', 'login', 'date_joined', 'last_login', 'is_active',
            'group', 'employee'
        ]
        read_only_fields = ['user_id', 'date_joined', 'last_login']

    def validate_login(self, value):
        cleaned = bleach.clean(value.strip(), tags=[], strip=True)
        return cleaned

    def create(self, validated_data):
        password = User.objects.make_random_password(length=12)
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        cleaned = bleach.clean(value.strip(), tags=[], strip=True)
        return cleaned

    def save(self):
        email = self.validated_data["email"]
        user = User.objects.get(employee__email=email)
        token = AccessToken.for_user(user) # generate token
        token.set_exp(lifetime=timedelta(minutes=10))
        reset_url = f"{settings.WEBSITE_URL}/reset/?token={str(token)}"
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password:\n{reset_url}\nThis link expires in 10 minutes.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False
        )
        return {"detail": "If the email exists, a password reset link has been sent."}


class ConfirmPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, max_length=128)

    def validate(self, data):
        token_str = data.get("token")
        try:
            untoken = UntypedToken(token_str)
            login = untoken.payload.get("login")
            user = User.objects.get(login=login)
            data["user"] = user
        except TokenError:
            raise serializers.ValidationError({"token": "Invalid or expired token."})
        except User.DoesNotExist:
            raise serializers.ValidationError({"token": "User not found."})
        return data

    def save(self):
        user = self.validated_data["user"]
        password = self.validated_data["password"]
        user.password = make_password(password)
        user.save()
        return {"detail": "Password has been reset successfully."}