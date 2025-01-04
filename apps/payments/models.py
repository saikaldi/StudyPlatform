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
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            # Create a unique slug combining timestamp and UUID
            unique_string = f"{self.bank}-{uuid.uuid4().hex[:6]}"
            self.slug = slugify(unique_string)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.bank} payment - {self.amount} - {self.status}"