from rest_framework import serializers
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
from .models import EmailConfirmation, Profile
from django.contrib.auth import authenticate
from ..OrtTest.serializers import UserStatistic as TUS
from ..OrtTest.serializers import UserStatisticSerializer as TUSS
from ..VideoCourse.serializers import UserStatistic as VUS
from ..VideoCourse.serializers import UserStatisticSerializer as VUSS

User = get_user_model()


# Сериализатор для регистрации
class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[EmailValidator()])
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField(min_length=8)
    user_status = serializers.ChoiceField(choices=User.STATUS_CHOICES)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    paid = serializers.ChoiceField(choices=User.PAID_CHOICES)

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return data

# Сериализатор для подтверждения регистрации
class ConfirmRegistrationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
            confirmation = EmailConfirmation.objects.get(user=user, code=data['code'])

            if confirmation.is_expired():
                user.delete()
                raise serializers.ValidationError("Код истёк")
        except (User.DoesNotExist, EmailConfirmation.DoesNotExist):
            raise serializers.ValidationError("Неверный код или email")
        return data

# Сериализатор для входа в систему
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Неправильный email или пароль")
        if not user.is_active:
            raise serializers.ValidationError("Аккаунт не активирован")
        return data

# Сериализатор для сброса пароля
class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")
        return data

# Сериализатор для смены пароля
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8)
    new_password_confirm = serializers.CharField(min_length=8)

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

# Сериализатор профиля
class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    # Добавляем информацию о пройденных тестах
    test_statistics = serializers.SerializerMethodField()
    video_statistics = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name', 'profile_picture', 'test_statistics', 'video_statistics'
        ]

    def get_test_statistics(self, obj):
        # Получаем статистику по тестам для текущего пользователя
        user = obj.user
        test_statistics = TUS.objects.filter(user=user)
        return TUSS(test_statistics, many=True).data

    def get_video_statistics(self, obj):
        # Получаем статистику по видео для текущего пользователя
        user = obj.user
        video_statistics = VUS.objects.filter(user=user, video__isnull=False)
        return VUSS(video_statistics, many=True).data

# class ProfileSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(source='user.email', read_only=True)
#     first_name = serializers.CharField(source='user.first_name', read_only=True)
#     last_name = serializers.CharField(source='user.last_name', read_only=True)
#     user_status = serializers.CharField(source='user.user_status', read_only=True)
#     paid = serializers.CharField(source='user.paid', read_only=True)

#     class Meta:
#         model = Profile
#         fields = ['email', 'first_name', 'last_name', 'profile_picture', 'address', 'date_of_birth', 'gender', 'user_status', 'paid']
#         read_only_fields = ['email', 'first_name', 'last_name', 'user_status', 'paid']
