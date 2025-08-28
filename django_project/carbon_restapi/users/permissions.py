from rest_framework.permissions import BasePermission

class HasAppPermission(BasePermission):
    app_label = 'users'
    perm_codename = None

    def has_permission(self, request, view):
        if not self.perm_codename:
            return False
        perm = f"{self.app_label}.{self.perm_codename}"
        return request.user.has_perm(perm)

class IsViewUserPermission(HasAppPermission):
    perm_codename = 'VIEW_USER'

class IsAddUserPermission(HasAppPermission):
    perm_codename = 'ADD_USER'

class IsDeleteUserPermission(HasAppPermission):
    perm_codename = 'DELETE_USER'

class IsModifyUserPermission(HasAppPermission):
    perm_codename = 'CHANGE_USER'