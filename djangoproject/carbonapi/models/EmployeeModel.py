
from django.db import models


class EmployeeStatus(models.Model):

    status_name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.status_name
    
    class Meta:
        db_table = 'Status'
        managed = True
        verbose_name = "Status"
        verbose_name_plural = "Status"
        default_permissions = []
        permissions = [
            ("view_status", "Can view employee status"),
            ("add_status", "Can add employee status"),
            ("change_status", "Can change employee status"),
            ("delete_status", "Can delete employee status")
        ]


class Employee(models.Model):

    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    status = models.ForeignKey(EmployeeStatus, on_delete=models.PROTECT, db_column='status')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'Employees'
        managed = True
        verbose_name = "Employee"
        verbose_name_plural = "Employees"
        default_permissions = []
        permissions = [
            ("view_employee", "Can view employee"),
            ("add_employee", "Can add employee"),
            ("change_employee", "Can change employee"),
            ("delete_employee", "Can delete employee")
        ]