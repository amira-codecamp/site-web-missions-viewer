from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from carbon_restapi.users.models import User, Group
from carbon_restapi.users.serializers import UserSerializer, GroupSerializer

from carbon_restapi.users.permissions import IsViewUserPermission, IsDeleteUserPermission, IsAddUserPermission, IsModifyUserPermission


class UserViewSet(viewsets.ViewSet):
    """
    RESTful Service for Users
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def list(self, request):
        """List all users."""
        if not IsViewUserPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.select_related('group', 'employee') # optimized query
        serializer = self.serializer_class(users, many=True)
        return Response({"users": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """Get current user's info."""
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def create(self, request):
        """Create a new user."""
        if not IsAddUserPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                return Response(self.serializer_class(user).data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        """
        Update an existing user.
        """
        if not IsModifyUserPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.select_related('group', 'employee').get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            return Response(self.serializer_class(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """Delete a user by primary key."""
        if not IsDeleteUserPermission().has_permission(request, self):
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ViewSet):
    """
    RestFUl Service for Groups
    """
    permission_classes = [IsAuthenticated]
    serializer_class = GroupSerializer

    def list(self, request):
        """List all groups."""
        groups = Group.objects.all()
        serializer = self.serializer_class(groups, many=True)
        return Response({"groups": serializer.data}, status=status.HTTP_200_OK)