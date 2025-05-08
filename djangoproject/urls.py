
from django.contrib import admin
from django.urls import path, include
from carbonapi.views.TripView import TripView


urlpatterns = [
    #path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('carbonapi/trips/', TripView.as_view(), name='trips'),
]