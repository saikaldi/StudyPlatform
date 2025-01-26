import django_filters
from django_filters import CharFilter, NumberFilter, DateFilter, ChoiceFilter, ModelChoiceFilter
from .models import Payment, PaymentService
from django.conf import settings
from django.contrib.auth import get_user_model


class PaymentServiceFilter(django_filters.FilterSet):
    payment_service_name = CharFilter(field_name='payment_service_name', lookup_expr='icontains')
    prop_number = CharFilter(field_name='prop_number', lookup_expr='icontains')
    full_name = CharFilter(field_name='full_name', lookup_expr='icontains')
    whatsapp_url = CharFilter(field_name='whatsapp_url', lookup_expr='icontains')
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = PaymentService
        fields = ['payment_service_name', 'prop_number', 'full_name', 'whatsapp_url', 'last_update_date', 'created_date']

class PaymentFilter(django_filters.FilterSet):
    user = ModelChoiceFilter(field_name='user', queryset=get_user_model().objects.all())
    slug = CharFilter(field_name='slug', lookup_expr='icontains')
    bank = ModelChoiceFilter(field_name='bank', queryset=PaymentService.objects.all())
    amount = NumberFilter(field_name='amount')
    phone_number = CharFilter(field_name='phone_number', lookup_expr='icontains')
    status = ChoiceFilter(field_name='status', choices=Payment.STATUS_CHOICES)
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = Payment
        fields = ['user', 'slug', 'bank', 'amount', 'phone_number', 'status', 'last_update_date', 'created_date']
