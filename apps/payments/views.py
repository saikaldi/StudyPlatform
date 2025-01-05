from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'slug'

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def verify_payment(self, request, slug=None):
        payment = self.get_object()
        if payment.status != 'PENDING':
            return Response(
                {"error": "Payment already processed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment.status = 'COMPLETED'
        payment.save()
        
        return Response({
            "message": "Payment verified successfully",
            "status": payment.status
        })

    @action(detail=True, methods=['post'])
    def reject_payment(self, request, slug=None):
        payment = self.get_object()
        if payment.status != 'PENDING':
            return Response(
                {"error": "Payment already processed"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment.status = 'FAILED'
        payment.save()
        
        return Response({
            "message": "Payment rejected",
            "status": payment.status
        })