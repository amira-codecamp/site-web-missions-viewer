from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from trips.models import Employee


class Permission(models.Model):
    permission_name = models.CharField(max_length=50, primary_key=True)
    permission_desc = models.CharField(max_length=255)  # Description of permission

    class Meta:
        db_table = 'Permissions'
        managed = True
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"
        default_permissions = []
        permissions = [
            ("view_permission", "Can view permission"),
            ("add_permission", "Can add permission"),
            ("change_permission", "Can change permission"),
            ("delete_permission", "Can delete permission")
        ]


class Group(models.Model):
    group_name = models.CharField(max_length=50, primary_key=True)
    permissions = models.ManyToManyField(Permission, through='Group_permission')  # Group permissions

    class Meta:
        db_table = 'Groups'
        managed = True
        verbose_name = "Group"
        verbose_name_plural = "Groups"
        default_permissions = []
        permissions = [
            ("view_group", "Can view group"),
            ("add_group", "Can add group"),
            ("change_group", "Can change group"),
            ("delete_group", "Can delete group")
        ]


class Group_permission(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, db_column='group')  # FK to Group
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT, db_column='permission')  # FK to Permission

    class Meta:
        db_table = 'Groups_permissions'
        managed = True
        verbose_name = "Group_permission"
        verbose_name_plural = "Groups_permissions"
        default_permissions = []
        permissions = [
            ("view_group_permission", "Can view group permission"),
            ("add_group_permission", "Can add group permission"),
            ("change_group_permission", "Can change group permission"),
            ("delete_group_permission", "Can delete group permission")
        ]


class User(AbstractBaseUser):
    login = models.CharField(max_length=50, primary_key=True)  # User login
    password = models.CharField(max_length=128)  # Hashed password
    date_joined = models.DateField()
    last_login = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, db_column='group')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, db_column='employee')

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    objects = BaseUserManager()

    def __str__(self):
        return self.login

    def has_perm(self, perm):
        # Check if user’s group has permission
        return self.group.permissions.filter(permission_name=perm).exists()

    class Meta:
        db_table = 'Users'
        managed = True
        verbose_name = "User"
        verbose_name_plural = "Users"
        default_permissions = []
        permissions = [
            ("view_user", "Can view user"),
            ("add_user", "Can add user"),
            ("change_user", "Can change user"),
            ("delete_user", "Can delete user")
        ]