from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.UserModel import User
from users.UserSerializer import UserSerializer

from users.UserPermission import IsViewUserPermission


class UserView(APIView):
    permission_classes = [IsAuthenticated, IsViewUserPermission]  # Require auth and 'view_user' perm

    def get(self, request):
        # Retrieve all users with related fields (optimized query)
        users = User.objects.select_related('group', 'employee').all()
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data}, status=status.HTTP_200_OK)  # Return serialized data