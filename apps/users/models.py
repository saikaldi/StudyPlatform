from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
import random
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Пользователь должен иметь email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = [
        ('manager', 'Менеджер'),
        ('student', 'Студент'),
        ('teacher', 'Мугалим'),
        ('admin', 'Админ'),
    ]
    PAID_CHOICES = [
        ('not_paid', 'Не оплачено'),
        ('paid', 'Оплачено'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    user_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='student')
    is_active = models.BooleanField(default=True)
    manager = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    student = models.BooleanField(default=False)
    teacher = models.BooleanField(default=False)
    paid = models.CharField(max_length=10, choices=PAID_CHOICES, default='not_paid')
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


# Profile Model
class Profile(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,13}$', message="Введите корректный номер телефона.")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=13, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('мужской', 'Мужской'), ('женский', 'Женский')], null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} профиль"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


# Email Confirmation Model
class EmailConfirmation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Код для пользователя: {self.user.email}'

    def is_expired(self):
        return now() > self.created_at + timedelta(minutes=10)

    @staticmethod
    def generate_code():
        return ''.join(random.choices('0123456789', k=6))

    class Meta:
        verbose_name = 'Код активации Аккаунта'
        verbose_name_plural = 'Коды активации Аккаунта'
