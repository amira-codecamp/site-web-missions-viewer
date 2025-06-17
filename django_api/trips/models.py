from django.db import models

# -----------------------------------
# Status model
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
# Employee model
# -----------------------------------
class Employee(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, db_column='status')

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
# Transport mode
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
# Mission grouping multiple trips
# -----------------------------------
class Mission(models.Model):
    mission_id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    mission_desc = models.CharField(max_length=255, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, db_column='employee')

    def __str__(self):
        return self.mission_num

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
# Trip Model
# -----------------------------------
class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True)
    departure_city = models.CharField(max_length=255)
    departure_country = models.CharField(max_length=255)
    destination_city = models.CharField(max_length=255)
    destination_country = models.CharField(max_length=255)
    is_round_trip = models.BooleanField()
    carpooling = models.IntegerField()
    
    mission = models.ForeignKey(Mission, on_delete=models.PROTECT, db_column='mission')
    transport = models.ForeignKey(Transport, on_delete=models.PROTECT, db_column='transport')

    carbon_footprint = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Trip {self.trip_id} from {self.departure_city} to {self.destination_city}"

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