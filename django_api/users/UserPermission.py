from rest_framework.permissions import BasePermission

class IsViewUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('view_user')
    
class IsDeleteUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('delete_user')
    
class IsAddUserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('add_user')