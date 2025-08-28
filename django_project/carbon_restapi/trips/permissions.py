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
    perm_codename = 'VIEW_EMPLOYEE'

class IsAddEmployeePermission(HasAppPermission):
    perm_codename = 'ADD_EMPLOYEE'

class IsModifyEmployeePermission(HasAppPermission):
    perm_codename = 'CHANGE_EMPLOYEE'

class IsViewTripPermission(HasAppPermission):
    perm_codename = 'VIEW_TRIP'

class IsAddTripPermission(HasAppPermission):
    perm_codename = 'ADD_TRIP'

class IsDeleteTripPermission(HasAppPermission):
    perm_codename = 'DELETE_TRIP'

class IsModifyTripPermission(HasAppPermission):
    perm_codename = 'CHANGE_TRIP'

class IsViewMissionPermission(HasAppPermission):
    perm_codename = 'VIEW_MISSION'

class IsAddMissionPermission(HasAppPermission):
    perm_codename = 'ADD_MISSION'

class IsDeleteMissionPermission(HasAppPermission):
    perm_codename = 'DELETE_MISSION'

class IsModifyMissionPermission(HasAppPermission):
    perm_codename = 'CHANGE_MISSION'