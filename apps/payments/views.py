from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail
from django.conf import settings
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, inline_serializer
from .models import Payment, PaymentService
from .serializers import PaymentSerializer, PaymentServiceSerializer
from rest_framework import serializers
import logging

logger = logging.getLogger(__name__)


@extend_schema(tags=['Payment Services'])
class PaymentServiceViewSet(viewsets.ModelViewSet):
    queryset = PaymentService.objects.all()
    serializer_class = PaymentServiceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @extend_schema(
        summary="Список всех платежных сервисов",
        description="Получение списка всех доступных платежных сервисов",
        responses={
            200: OpenApiResponse(
                description="Успешный ответ",
                response=PaymentServiceSerializer(many=True)
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание нового платежного сервиса",
        description="Создание нового платежного сервиса в системе",
        request=PaymentServiceSerializer,
        responses={
            201: OpenApiResponse(
                description="Создан новый платежный сервис",
                response=PaymentServiceSerializer
            ),
            400: OpenApiResponse(
                description="Ошибка валидации данных",
                examples=[OpenApiExample("Ошибка валидации", value={"payment_service_name": ["Это поле обязательно"]})]
            )
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

@extend_schema(tags=['Payments'])
class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().order_by('-created_date')
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

    @extend_schema(
        summary="Список всех платежей",
        description="Получение списка платежей. Для администраторов доступны все платежи, остальным - только свои",
        responses={
            200: OpenApiResponse(
                description="Список платежей",
                response=PaymentSerializer(many=True)
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание нового платежа",
        description="Создание нового платежа в системе",
        request=PaymentSerializer,
        responses={
            201: OpenApiResponse(
                description="Платеж создан",
                response=PaymentSerializer
            ),
            400: OpenApiResponse(
                description="Ошибка валидации данных",
                examples=[
                    OpenApiExample("Ошибка номера телефона", value={"phone_number": ["Телефонный номер должен начинаться с +996"]}),
                    OpenApiExample("Ошибка суммы", value={"amount": ["Сумма должна быть больше 0"]})
                ]
            )
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление статуса платежа",
        description="Обновление статуса платежа. Доступно только для администраторов",
        request=inline_serializer(
            "UpdateStatusSerializer",
            fields={
                "status": serializers.ChoiceField(choices=Payment.STATUS_CHOICES),
            },
        ),
        responses={
            200: OpenApiResponse(
                description="Статус успешно обновлен",
                examples=[OpenApiExample("Успешное обновление", value={"status": "Статус успешно обновлен с PENDING на COMPLETED"})]
            ),
            400: OpenApiResponse(
                description="Недопустимый статус или ошибка",
                examples=[OpenApiExample("Недопустимый статус", value={"error": "Недопустимый статус"})]
            )
        }
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser], url_path='update_status')
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
