from carbon_restapi.trips.models import Trip, Mission, Employee
from django_filters import rest_framework as filters
from django_filters.filters import BaseInFilter, NumberFilter


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class TripFilter(filters.FilterSet):
    year = filters.BaseInFilter(field_name='mission__start_date__year', lookup_expr='in')
    employee_id = NumberInFilter(field_name="mission__employee__employee_id", lookup_expr='in')
    mission_id = NumberInFilter(field_name="mission__mission_id", lookup_expr='in')

    class Meta:
        model = Trip
        fields = ['year', 'employee_id', 'mission_id']


class MissionFilter(filters.FilterSet):
    year = filters.BaseInFilter(field_name='start_date__year', lookup_expr='in')
    employee_id = NumberInFilter(field_name="employee__employee_id", lookup_expr='in')

    class Meta:
        model = Mission
        fields = ['year', 'employee_id']


class EmployeeFilter(filters.FilterSet):
    status = filters.CharFilter(field_name='status', lookup_expr='iexact')
    research_team = filters.CharFilter(field_name='research_team', lookup_expr='iexact')

    class Meta:
        model = Employee
        fields = ['status', 'research_team']