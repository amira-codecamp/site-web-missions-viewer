from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from carbon_restapi.users.models import User, Group
from carbon_restapi.users.serializers import UserSerializer, GroupSerializer
from carbon_restapi.users.permissions import (
    IsViewUserPermission, IsDeleteUserPermission,
    IsAddUserPermission, IsModifyUserPermission
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    """
    queryset = User.objects.select_related('group', 'employee').all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    swagger_tags = ['users']

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsViewUserPermission]
        elif self.action == 'create':
            permission_classes = [IsAuthenticated, IsAddUserPermission]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsModifyUserPermission]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsDeleteUserPermission]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Group model (read-only).
    """
    http_method_names = ['get', 'head', 'options']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]
    swagger_tags = ['groups']