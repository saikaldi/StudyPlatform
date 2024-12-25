from rest_framework import serializers
from django.core.validators import EmailValidator
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import EmailConfirmation, Profile
from django.contrib.auth import authenticate

User = get_user_model()


# Сериализатор для регистрации
class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[EmailValidator()])
    password = serializers.CharField(min_length=8)
    password_confirm = serializers.CharField(min_length=8)

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
                raise serializers.ValidationError(f"Код истёк")
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

class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['email', 'profile_picture', 'first_name', 'last_name', 'address', 'date_of_birth', 'gender']
        read_only_fields = ['email'] 
