from carbon_restapi.trips.models import Trip, Mission
from django_filters import rest_framework as filters
from django_filters.filters import BaseInFilter, NumberFilter


class NumberInFilter(BaseInFilter, NumberFilter):
    pass


class TripFilter(filters.FilterSet):
    year = filters.BaseInFilter(field_name='mission__start_date__year', lookup_expr='in')
    # year = filters.NumberFilter(field_name="mission__start_date", lookup_expr='year')
    employee_id = NumberInFilter(field_name="mission__employee__employee_id", lookup_expr='in')
    mission_id = NumberInFilter(field_name="mission__mission_id", lookup_expr='in')

    class Meta:
        model = Trip
        fields = ['year', 'employee_id', 'mission_id']