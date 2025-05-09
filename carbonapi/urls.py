
from django.urls import path, include
from tripsservice.views.TripView import TripView


urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/trips/', TripView.as_view(), name='trips'),
]