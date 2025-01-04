from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'bank', 'amount', 'phone_number', 'status', 'created_at']
        read_only_fields = ['status', 'created_at']

    def validate_phone_number(self, value):
        if not value.startswith('+996'):
            raise serializers.ValidationError("Phone number must start with +996")
        if not len(value) == 13:
            raise serializers.ValidationError("Invalid phone number length")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than 0")
        return value