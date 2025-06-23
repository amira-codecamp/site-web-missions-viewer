from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from trips.models import Employee

from users.UserModel import User, Group
from users.UserSerializer import UserSerializer, GroupSerializer

from users.UserPermission import IsViewUserPermission, IsDeleteUserPermission, IsAddUserPermission, IsModifyUserPermission


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

        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(user_id=user_id)
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
    
    # PUT: Update User
    def put(self, request):
        # Permission check
        if not IsModifyUserPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        user_id = request.data.get('user_id')
        if not user_id:
            return Response({'error': 'user_id is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try: # Get user row
            user = User.objects.get(user_id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        if data['password'] == '*****':
            data['password'] = user.password # keep user password

        # Pass request.data with partial=True for partial update
        serializer = UserSerializer(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # <-- calls custom update method internally

        return Response(serializer.data, status=status.HTTP_200_OK)


# View to retrieve groups
class GroupView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response({"groups": serializer.data}, status=status.HTTP_200_OK)