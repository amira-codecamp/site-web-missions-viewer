from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from carbon_restapi.users.views import (
    UserViewSet, GroupViewSet, PasswordResetViewSet, ConfirmPasswordViewSet
)

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

# Reset password endpoints
router.register(r'resetPassword', PasswordResetViewSet, basename='resetPassword')
router.register(r'confirmPassword', ConfirmPasswordViewSet, basename='confirmPassword')

# Trips endpoints
router.register(r'status', StatusViewSet, basename='status')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'transports', TransportViewSet, basename='transport')
router.register(r'trips', TripViewSet, basename='trip')
router.register(r'missions', MissionViewSet, basename='mission')

schema_view = get_schema_view(
   openapi.Info(
      title="Carbon API",
      default_version='v1',
      description="API documentation for the Carbon application",
      contact=openapi.Contact(email="lacroix@lipn.fr"),
      #terms_of_service="https://www.google.com/policies/terms/",
      #license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('carbon/', include(router.urls)),
    path('token/', include('djoser.urls.jwt')),       # JWT endpoints

    # Swagger/OpenAPI docs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]