from django.db import models
from django.conf import settings
from django.utils.text import slugify
import uuid

class Payment(models.Model):
    BANK_CHOICES = [
        ('MBANK', 'MBank'),
        ('OBANK', 'O!Bank'),
        ('ELDIK', 'Элдик Банк'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    bank = models.CharField(max_length=10, choices=BANK_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Сумма оплаты
    phone_number = models.CharField(max_length=15)  # Номер телефона
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')# Статус оплаты
    created_at = models.DateTimeField(auto_now_add=True)# Дата создания
    updated_at = models.DateTimeField(auto_now=True)# Дата обновления

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            # Уникальный slug для платежа
            unique_string = f"{self.bank}-{uuid.uuid4().hex[:6]}"
            self.slug = slugify(unique_string)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bank} payment - {self.amount} - {self.status}"
    



class PaymentMethod(models.Model):
    payment_service_name = models.CharField(max_length=100)  # Название сервиса
    service_logo = models.ImageField(upload_to="payments_service_logos/", blank=True, null=True) # Логотип
    qr_code = models.ImageField(upload_to='payment_qr_codes/', blank=True, null=True) # QR-код
    req_number = models.CharField(max_length=30, blank=True, null=True)  # Номер реквизита
    full_name = models.CharField(max_length=100, blank=True, null=True)
    whatsapp_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.payment_service_name