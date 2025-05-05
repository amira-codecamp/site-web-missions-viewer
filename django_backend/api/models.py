from django.db import models


class StaffStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status_name = models.CharField(max_length=255)

    def __str__(self):
        return self.status_name
    
    class Meta:
        db_table = 'StaffStatus'
        managed = True
        verbose_name = "StaffStatus"
        verbose_name_plural = "StaffStatus"


class Employees(models.Model):
    employee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    status = models.ForeignKey(StaffStatus, on_delete=models.PROTECT, related_name='employees')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'Employees'
        managed = True
        verbose_name = "Employee"
        verbose_name_plural = "Employees"


class Missions(models.Model):
    mission_id = models.AutoField(primary_key=True)
    mission_adm_num = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    mission_reason = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.mission_adm_num
    
    class Meta:
        db_table = 'Missions'
        managed = True
        verbose_name = "Mission"
        verbose_name_plural = "Missions"


class TransportationModes(models.Model):
    transportation_id = models.AutoField(primary_key=True)
    transportation_name = models.CharField(max_length=255)

    def __str__(self):
        return self.transportation_name
    
    class Meta:
        db_table = 'TransportationModes'
        managed = True
        verbose_name = "TransportationMode"
        verbose_name_plural = "TransportationModes"


class Trips(models.Model):
    trip_id = models.AutoField(primary_key=True)
    trip_date = models.DateField(null=True, blank=True)
    departure_city = models.CharField(max_length=255)
    departure_country = models.CharField(max_length=255)
    destination_city = models.CharField(max_length=255)
    destination_country = models.CharField(max_length=255)
    trip_reason = models.CharField(max_length=255, null=True, blank=True)
    is_round_trip = models.BooleanField(null=True, blank=True)
    carpooling = models.IntegerField(null=True, blank=True)
    transportation = models.ForeignKey(TransportationModes, on_delete=models.PROTECT, related_name='trips')
    mission = models.ForeignKey(Missions, on_delete=models.PROTECT, related_name='trips')
    employee = models.ForeignKey(Employees, on_delete=models.PROTECT, related_name='trips')
    carbon_footprint = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Trip {self.trip_id} from {self.departure_city} to {self.destination_city}"
    
    class Meta:
        db_table = 'Trips'
        managed = True
        verbose_name = "Trip"
        verbose_name_plural = "Trips"