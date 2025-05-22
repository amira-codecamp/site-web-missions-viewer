
from rest_framework.permissions import BasePermission


class IsViewAllTransportPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('view_all_transport')