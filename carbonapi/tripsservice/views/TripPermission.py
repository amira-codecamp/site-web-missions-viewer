
from rest_framework.permissions import BasePermission


class IsViewAllTripPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('view_all_trip')


class IsViewTripPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('view_trip')