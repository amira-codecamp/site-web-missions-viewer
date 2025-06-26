from rest_framework.permissions import BasePermission

class HasAppPermission(BasePermission):
    app_label = 'trips'
    perm_codename = None

    def has_permission(self, request, view):
        if not self.perm_codename:
            return False
        perm = f"{self.app_label}.{self.perm_codename}"
        return request.user.has_perm(perm)

class IsViewEmployeePermission(HasAppPermission):
    perm_codename = 'view_employee'

class IsModifyEmployeePermission(HasAppPermission):
    perm_codename = 'change_employee'

class IsViewTripPermission(HasAppPermission):
    perm_codename = 'view_trip'

class IsAddTripPermission(HasAppPermission):
    perm_codename = 'add_trip'

class IsDeleteTripPermission(HasAppPermission):
    perm_codename = 'delete_trip'

class IsModifyTripPermission(HasAppPermission):
    perm_codename = 'change_trip'

class IsViewMissionPermission(HasAppPermission):
    perm_codename = 'view_mission'

class IsAddMissionPermission(HasAppPermission):
    perm_codename = 'add_mission'

class IsDeleteMissionPermission(HasAppPermission):
    perm_codename = 'delete_mission'

class IsModifyMissionPermission(HasAppPermission):
    perm_codename = 'change_mission'