from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid


class PaymentService(models.Model):
    payment_service_name = models.CharField(max_length=100, verbose_name='Названия сервиса')  # Название сервиса
    service_logo = models.ImageField(upload_to="payments_service_logos/", blank=True, null=True, verbose_name='Логотип сервиса') # Логотип
    qr_code = models.ImageField(upload_to='payment_qr_codes/', blank=True, null=True, verbose_name='QR код для оплаты') # QR-код
    prop_number = models.CharField(max_length=30, blank=True, null=True, verbose_name='Номер реквезита')  # Номер реквизита
    full_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='Имя Владельца карты')
    whatsapp_url = models.TextField(blank=True, null=True, verbose_name='Ссылка на WhatsApp')
    last_update_date = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.payment_service_name

    class Meta:
        verbose_name = "Сервис для оплаты"
        verbose_name_plural = "Сервисы для оплаты"
        ordering = ['-created_date']

class Payment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, verbose_name='Пользователь')
    slug = models.SlugField(max_length=250, unique=True, blank=True, verbose_name='slug')
    bank = models.ForeignKey(PaymentService, on_delete=models.CASCADE, verbose_name='Сервис для оплаты')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма оплаты') # Сумма оплаты
    phone_number = models.CharField(max_length=15, verbose_name='Номер телефона')  # Номер телефона
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING', verbose_name='Статус оплаты') # Статус оплаты
    last_update_date = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
        ordering = ['-created_date']

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_string = f"{self.bank}-{uuid.uuid4().hex[:6]}"
            self.slug = slugify(unique_string)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bank} payment - {self.amount} - {self.status}"
