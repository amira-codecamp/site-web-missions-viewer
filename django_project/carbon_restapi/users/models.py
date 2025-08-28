from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from carbon_restapi.trips.models import Employee
from django.utils.crypto import get_random_string


# -----------------------------------
# Custom permission model
# -----------------------------------
class Permission(models.Model):
    permission_name = models.CharField(max_length=50, primary_key=True)
    permission_desc = models.CharField(max_length=255)

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

    def __str__(self):
        return self.permission_name


# -----------------------------------
# Group model with many-to-many permission relationship
# -----------------------------------
class Group(models.Model):
    group_name = models.CharField(max_length=50, primary_key=True)
    permissions = models.ManyToManyField(Permission, through='GroupPermission')

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

    def __str__(self):
        return self.group_name


# -----------------------------------
# Through model for Group-Permission mapping
# -----------------------------------
class GroupPermission(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, db_column='group', related_name='group_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.PROTECT, db_column='permission', related_name='permission_groups')

    class Meta:
        db_table = 'GroupPermissions'
        managed = True
        verbose_name = "Group Permission"
        verbose_name_plural = "Group Permissions"
        default_permissions = []
        permissions = [
            ("view_group_permission", "Can view group permission"),
            ("add_group_permission", "Can add group permission"),
            ("change_group_permission", "Can change group permission"),
            ("delete_group_permission", "Can delete group permission")
        ]


# -----------------------------------
# Custom user manager for creating users and superusers
# -----------------------------------
class UserManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError("The login must be set")
        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return self.create_user(login, password, **extra_fields)

    def make_random_password(self, length=10,
                            allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
        return get_random_string(length, allowed_chars)


# -----------------------------------
# Custom User model linked to Group and Employee
# -----------------------------------
class User(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    group = models.ForeignKey(Group, on_delete=models.PROTECT, db_column='group', related_name='users')
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, db_column='employee', related_name='users')

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.login

    def has_perm(self, perm, obj=None):
        """
        Check if the user's group has a specific permission.
        Supports both 'perm_codename' and 'app_label.perm_codename' formats.
        """
        codename = perm.split('.')[-1]  # Support 'app_label.codename' and plain codename
        return self.group.permissions.filter(permission_name=codename).exists()

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