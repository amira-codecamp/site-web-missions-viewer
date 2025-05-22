
from django.db import models


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
            ("delete_transport", "Can delete transport"),
            ("view_all_transport", "Can view all transports"),
        ]