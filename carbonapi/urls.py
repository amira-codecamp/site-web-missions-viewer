
from django.urls import path, include
from tripsservice.views.TripView import TripView, MissionView
from tripsservice.views.TransportView import TransportView
from tripsservice.views.EmployeeView import EmployeeView
from emissionsservice.views.TravelEmissionView import TravelEmissionView


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('api/trips/', TripView.as_view(), name='trips'),
    path('api/employees/', EmployeeView.as_view(), name='employees'),
    path('api/transports/', TransportView.as_view(), name='transports'),
    path('api/missions/', MissionView.as_view(), name='missions'),

    path('emissions/travel/', TravelEmissionView.as_view(), name='travel_emissions'),
]