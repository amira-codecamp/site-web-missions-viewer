from django.contrib import admin
from django.contrib.auth.models import Group
from users.models import UsersAccounts
from users.forms import UsersAccountsAdminForm
from api.models import Employees, StaffStatus, Trips, Missions, TransportationModes


admin.site.unregister(Group)

@admin.register(UsersAccounts)
class UsersAccountsAdmin(admin.ModelAdmin):
    form = UsersAccountsAdminForm

admin.site.register(Employees)
admin.site.register(StaffStatus)
admin.site.register(Trips)
admin.site.register(Missions)
admin.site.register(TransportationModes)