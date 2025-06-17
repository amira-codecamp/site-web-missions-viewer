from django.urls import path, include

from trips.views import TripView, MissionView, TransportView, EmployeeView

from users.UserView import UserView

from carbon.CarbonView import CarbonView


urlpatterns = [
    # Authentication endpoints by djoser
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),

    path('api/users/', UserView.as_view(), name='users'),  # Custom user view

    # API endpoints for trips
    path('api/trips/', TripView.as_view(), name='trips'),
    path('api/employees/', EmployeeView.as_view(), name='employees'),
    path('api/transports/', TransportView.as_view(), name='transports'),
    path('api/missions/', MissionView.as_view(), name='missions'),

    # Endpoint for carbon
    path('api/carbon/', CarbonView.as_view(), name='carbon'),
]