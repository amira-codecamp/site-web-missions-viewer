from django.urls import path, include
from rest_framework.routers import DefaultRouter
from carbon_restapi.users.views import UserViewSet, GroupViewSet
from carbon_restapi.trips.views import (
    StatusViewSet,
    EmployeeViewSet,
    TransportViewSet,
    TripViewSet,
    MissionViewSet
)

router = DefaultRouter()

# Users endpoints
router.register(r'users', UserViewSet, basename='user')
router.register(r'groups', GroupViewSet, basename='group')

# Trips endpoints
router.register(r'status', StatusViewSet, basename='status')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'transports', TransportViewSet, basename='transport')
router.register(r'trips', TripViewSet, basename='trip')
router.register(r'missions', MissionViewSet, basename='mission')

urlpatterns = [
    path('carbon/', include(router.urls)),
    path('token/', include('djoser.urls')),           # Basic Djoser endpoints
    path('token/', include('djoser.urls.jwt')),       # JWT endpoints
]