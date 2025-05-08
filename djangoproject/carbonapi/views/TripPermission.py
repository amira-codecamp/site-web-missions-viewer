
from rest_framework.permissions import BasePermission


class IsViewTripPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('view_trip')