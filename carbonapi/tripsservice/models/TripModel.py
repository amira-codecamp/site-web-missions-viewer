
from django.db import models
from tripsservice.models.EmployeeModel import Employee
from tripsservice.models.TransportModel import Transport


class Mission(models.Model):

    mission_num = models.CharField(max_length=50, primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    mission_desc = models.CharField(max_length=255)

    def __str__(self):
        return self.mission_adm_num
    
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
    employee = models.ForeignKey(Employee, on_delete=models.PROTECT, db_column='employee')
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