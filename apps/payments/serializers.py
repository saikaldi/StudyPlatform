from rest_framework import serializers
from .models import Payment, PaymentMethod

class PaymentSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'slug', 'payment_service_name','service_logo', 'qr_code','req_number',
                   'full_name', 'amount', 'phone_number', 'status', 'created_at', 'updated_at'
                   ]
        
        read_only_fields = ['status', 'created_at','updated_at', 'slug']

    def validate_phone_number(self, value):
        if not value.startswith('+996'):
            raise serializers.ValidationError("Телефон номери төмөнкү менен башталышы керек +996")
        if not len(value) == 13:
            raise serializers.ValidationError("Телефон номери узундугу туура эмес")
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Сумма 0дөн чоң болушу керек")
        return value
    

class PaymentMethodSerializers(serializers.Serializer):
    class Meta:
        model = PaymentMethod
        fields = [
            'id', 'payment_service_name', 'service_logo', 'qr_code',
            'req_number', 'full_name', 'whatsapp_url'
        ]
    