from rest_framework.permissions import BasePermission


# Check if user can view employees
class IsViewEmployeePermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('view_employee')

# Check if user can view trips
class IsViewTripPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('view_trip')

# Check if user can add trips
class IsAddTripPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('add_trip')

# Check if user can delete trips
class IsDeleteTripPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('delete_trip')

# Check if user can modify trips
class IsModifyTripPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('change_trip')

# Check if user can view missions
class IsViewMissionPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('view_mission')

# Check if user can add missions
class IsAddMissionPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('add_mission')