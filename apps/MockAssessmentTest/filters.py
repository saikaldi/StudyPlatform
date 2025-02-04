import django_filters
from django_filters import CharFilter, BooleanFilter, ChoiceFilter, DateFilter
from .models import MockAssessmentTest


class MockAssessmentTestFilter(django_filters.FilterSet):
    first_name = CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = CharFilter(field_name='last_name', lookup_expr='icontains')
    phone_number = CharFilter(field_name='phone_number', lookup_expr='icontains')
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = MockAssessmentTest
        fields = ['first_name', 'last_name', 'phone_number', 'last_update_date', 'created_date']
