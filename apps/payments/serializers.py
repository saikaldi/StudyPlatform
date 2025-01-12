from rest_framework import serializers
from .models import Payment, PaymentService


class PaymentSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'slug', 'bank', 'amount', 'phone_number', 'status', 'last_update_date', 'created_date']
        read_only_fields = ['last_update_date', 'created_date', 'slug']

    def validate_phone_number(self, value):
        if not value.startswith('+996'):
            raise serializers.ValidationError("Телефонный номер должен начинаться с +996")
        if len(value) != 13:
            raise serializers.ValidationError("Длина телефонного номера неверна")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма должна быть больше 0")
        return value

class PaymentServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentService
        fields = ['id', 'payment_service_name', 'service_logo', 'qr_code', 'prop_number', 'full_name', 'whatsapp_url']
        read_only_fields = ['last_update_date', 'created_date']
