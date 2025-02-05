import django_filters
from django_filters import CharFilter, BooleanFilter, ChoiceFilter, DateFilter
from .models import Profile, EmailConfirmation


class ProfileFilter(django_filters.FilterSet):
    first_name = CharFilter(field_name='user__first_name', lookup_expr='icontains')
    last_name = CharFilter(field_name='user__last_name', lookup_expr='icontains')
    email = CharFilter(field_name='user__email', lookup_expr='icontains')
    phone_number = CharFilter(field_name='phone_number', lookup_expr='icontains')
    last_update_date = DateFilter(field_name='created_at', lookup_expr='date')
    created_date = DateFilter(field_name='created_at', lookup_expr='date')

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'last_update_date', 'created_date']

class EmailConfirmationFilter(django_filters.FilterSet):
    user = CharFilter(field_name='user__email', lookup_expr='icontains')
    code = CharFilter(field_name='code')
    created_at = DateFilter(field_name='created_at', lookup_expr='date')
    is_used = BooleanFilter(field_name='is_used')

    class Meta:
        model = EmailConfirmation
        fields = ['user', 'code', 'created_at', 'is_used']
