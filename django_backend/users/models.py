from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Permission
from django.db import models
from api.models import Employees
from django.contrib.auth.password_validation import validate_password


class UsersAccountsManager(BaseUserManager):
    def create_user(self, login, password=None, **extra_fields):
        if not login:
            raise ValueError("Field login must be set") 
        
        if password:
            validate_password(password)

        user = self.model(login=login, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, login, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        validate_password(password)
        return self.create_user(login, password, **extra_fields)


class UsersAccounts(AbstractBaseUser):
    login = models.CharField(max_length=255, primary_key=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    employee = models.ForeignKey(Employees, on_delete=models.PROTECT, related_name='usersaccounts', null=True, blank=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []

    objects = UsersAccountsManager()

    def __str__(self):
        return self.login
    
    @property
    def is_superuser(self):
        return self.is_admin
    
    @property
    def is_staff(self):
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        if self.is_admin:
            return True
        return False

    def has_module_perms(self, app_label):
        if self.is_admin:
            return True
        return False
    
    class Meta:
        db_table = 'UsersAccounts'
        managed = True
        verbose_name = "Account"
        verbose_name_plural = "Accounts"