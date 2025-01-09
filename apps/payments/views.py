from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail
from django.conf import settings
from .models import Payment, PaymentService
from .serializers import PaymentSerializer, PaymentServiceSerializer
import logging

logger = logging.getLogger(__name__)


class PaymentServiceViewSet(viewsets.ModelViewSet):
    queryset = PaymentService.objects.all()
    serializer_class = PaymentServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-created_at')
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(user=user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        payment = self.get_object()
        new_status = request.data.get('status')

        if new_status not in dict(Payment.STATUS_CHOICES):
            return Response({'error': 'Недопустимый статус'}, status=400)

        old_status = payment.status
        payment.status = new_status
        payment.save()

        user_email = payment.user.email
        if user_email:
            self._send_status_update_email(user_email, payment, new_status)

        return Response({'status': f'Статус успешно обновлен с {old_status} на {new_status}'})

    def _send_status_update_email(self, email, payment, new_status):
        subject = f"Изменение статуса вашей оплаты - {payment.slug}"
        status_messages = {
            'PENDING': 'Оплата обрабатывается',
            'COMPLETED': 'Оплата успешно завершена',
            'FAILED': 'Оплата отклонена'
        }
        message = f"Статус вашей оплаты изменен на: {status_messages.get(new_status, 'Неизвестный')}"
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            logger.info(f"Уведомление успешно отправлено пользователю: {email}")
        except Exception as e:
            logger.error(f"Ошибка отправки email пользователю: {e}")
