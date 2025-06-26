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
    perm_codename = 'view_user'

class IsAddUserPermission(HasAppPermission):
    perm_codename = 'add_user'

class IsDeleteUserPermission(HasAppPermission):
    perm_codename = 'delete_user'

class IsModifyUserPermission(HasAppPermission):
    perm_codename = 'change_user'