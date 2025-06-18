from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from trips.models import Employee

from users.UserModel import User, Group
from users.UserSerializer import UserSerializer

from users.UserPermission import IsViewUserPermission, IsDeleteUserPermission, IsAddUserPermission


class UserView(APIView):
    permission_classes = [IsAuthenticated]  # Requires authentication

    def get(self, request):
        if not IsViewUserPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Retrieve all users with related fields (optimized query)
        users = User.objects.select_related('group', 'employee').all()
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data}, status=status.HTTP_200_OK)  # Return serialized data
    
    # Delete an existing user
    def delete(self, request):
        if not IsDeleteUserPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        user_login = request.data.get('login')
        if not user_login:
            return Response({'error': 'user_login is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(login=user_login)
            user.delete()
            return Response({'message': 'User deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
    # POST: Create a new user
    def post(self, request):
        if not IsAddUserPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            except (Employee.DoesNotExist, Group.DoesNotExist) as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)