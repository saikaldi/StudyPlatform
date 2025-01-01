from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
import random
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


# Кастомный менеджер модели пользователя
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
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

# Модель пользователя
class User(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = [
        ('Менеджер', 'Менеджер'),
        ('Студент', 'Студент'),
        ('Мугалим', 'Мугалим'),
        ('Админ', 'Админ'),
    ]                                                                                               # Варианты статуса пользователя
    PAID_CHOICES = [
        ('Не оплачено', 'Не оплачено'),
        ('Оплачено', 'Оплачено'),
    ]                                                                                               # Варианты статуса оплаты
    first_name = models.CharField(max_length=50)                                                    # Имя пользователя
    last_name = models.CharField(max_length=50)                                                     # Фамилия пользователя
    email = models.EmailField(unique=True)                                                          # Электронная почта пользователя
    user_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Студент')        # Статусы пользователей
    paid = models.CharField(max_length=11, choices=PAID_CHOICES, default='Не оплачено')             # Статус оплаты
    is_status_approved = models.BooleanField(default=False)

    is_staff = models.BooleanField(default=False)                                                   # Для доступа в админку
    is_active = models.BooleanField(default=False)                                                   # Для управления статусом активности
    date_joined = models.DateTimeField(auto_now_add=True)                                           # Дата регистрации пользователя

    objects = UserManager()                                                                         # Менеджер для управления User
    USERNAME_FIELD = 'email'                                                                        # Никальный идентификатор пользователя
    REQUIRED_FIELDS = []                                                                            # Обязательные поля для модели User

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

# Модель профиля
class Profile(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,13}$', message="Введите корректный номер телефона")                         # Валидатор номера телефона
    user = models.OneToOneField(User, on_delete=models.CASCADE)                                                                 # К какому пользователю пренадлежит Профиль
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)                                   # Фото профиля пользователя
    address = models.CharField(max_length=100, blank=True, null=True)                                                           # Адрес пользователя
    phone_number = models.CharField(validators=[phone_regex], max_length=13, unique=True, blank=True, null=True)                # Номер телефона пользователя
    date_of_birth = models.DateField(null=True, blank=True)                                                                     # Дата рождения пользователя
    gender = models.CharField(max_length=10, choices=[('мужской', 'Мужской'), ('женский', 'Женский')], null=True, blank=True)   # Пол пользователя

    def __str__(self):
        return f"{self.user.email} профиль"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

# Функция для автоматического создания профиля пользователя 
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

# Подтверждения аккаунта по Email
class EmailConfirmation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)                    # Пользователь к которому приадлежит код подтверждения
    code = models.CharField(max_length=6)                                                           # Код подтверждения
    created_at = models.DateTimeField(auto_now_add=True)                                            # Дата выдачи кода
    is_used = models.BooleanField(default=False)

    # Функция проверки времени жизни кода
    def is_expired(self):
        return now() > self.created_at + timedelta(minutes=10)

    # Функция генерации кода
    @staticmethod
    def generate_code():
        return ''.join(random.choices('0123456789', k=6))

    def __str__(self):
        return f'Код для пользователя: {self.user.email}'

    class Meta:
        verbose_name = 'Код активации Аккаунта'
        verbose_name_plural = 'Коды активации Аккаунта'

class MockAssessmentTest(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,13}$', message="Введите корректный номер телефона")                         # Валидатор номера телефона
    phone_number = models.CharField(validators=[phone_regex], max_length=13, unique=True, blank=True, null=True)                # Номер телефона пол
    first_name = models.CharField(max_length=50)                                                                                # Имя пользователя
    last_name = models.CharField(max_length=50)                                                                                 # Фамилия пользователя

    def __str__(self):
        return f'Данные пользователя: {self.first_name} - {self.last_name} - {self.phone_number}'

    class Meta:
        verbose_name = 'Пробная запись на оценочный тест'
        verbose_name_plural = 'Пробные записи на оценочные тесты'




