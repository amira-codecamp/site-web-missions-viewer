from django.db import models
from carbon_restapi.trips.utils import TripUtils

# -----------------------------------
# Status model for employee state (e.g., Researcher, Intern)
# -----------------------------------
class Status(models.Model):
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
            ("view_status", "Can view status"),
            ("add_status", "Can add status"),
            ("change_status", "Can change status"),
            ("delete_status", "Can delete status")
        ]


# -----------------------------------
# Employee model linked to a status
# -----------------------------------
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, db_column='status', related_name='employees')

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


# -----------------------------------
# Transport model for travel modes
# -----------------------------------
class Transport(models.Model):
    transport_name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.transport_name

    class Meta:
        db_table = 'Transports'
        managed = True
        verbose_name = "Transport"
        verbose_name_plural = "Transports"
        default_permissions = []
        permissions = [
            ("view_transport", "Can view transport"),
            ("add_transport", "Can add transport"),
            ("change_transport", "Can change transport"),
            ("delete_transport", "Can delete transport")
        ]


# -----------------------------------
# Mission model representing a business trip container
# -----------------------------------
class Mission(models.Model):
    mission_id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    mission_desc = models.CharField(max_length=255, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, db_column='employee', related_name='missions')

    def __str__(self):
        return self.mission_desc

    class Meta:
        db_table = 'Missions'
        managed = True
        verbose_name = "Mission"
        verbose_name_plural = "Missions"
        default_permissions = []
        permissions = [
            ("view_mission", "Can view mission"),
            ("add_mission", "Can add mission"),
            ("change_mission", "Can change mission"),
            ("delete_mission", "Can delete mission")
        ]


# -----------------------------------
# Trip model linked to a mission and transport mode
# -----------------------------------
class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True)
    departure_city = models.CharField(max_length=255)
    departure_country = models.CharField(max_length=2)
    destination_city = models.CharField(max_length=255)
    destination_country = models.CharField(max_length=2)
    is_round_trip = models.BooleanField()
    carpooling = models.PositiveIntegerField()  # Number of people carpooled

    mission = models.ForeignKey(Mission, on_delete=models.PROTECT, db_column='mission', related_name='trips')
    transport = models.ForeignKey(Transport, on_delete=models.PROTECT, db_column='transport', related_name='trips')

    carbon_footprint = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def __str__(self):
        return f"Trip {self.trip_id}: {self.departure_city} → {self.destination_city}"

    def save(self, *args, **kwargs):
        carbon = TripUtils().compute_footprint(self)
        if carbon is not None:
            self.carbon_footprint = round(carbon, 2)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'Trips'
        managed = True
        verbose_name = "Trip"
        verbose_name_plural = "Trips"
        default_permissions = []
        permissions = [
            ("view_trip", "Can view trip"),
            ("add_trip", "Can add trip"),
            ("change_trip", "Can change trip"),
            ("delete_trip", "Can delete trip")
        ]