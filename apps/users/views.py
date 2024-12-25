from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import EmailConfirmation, Profile
from .serializers import ProfileSerializer, RegisterSerializer, ConfirmRegistrationSerializer, LoginSerializer, RequestPasswordResetSerializer, ResetPasswordSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample

User = get_user_model()


# ================== Регистрация пользователя ==================
@extend_schema(
    summary="Регистрация пользователя",
    description="Создание нового пользователя с отправкой кода подтверждения на email",
    request=RegisterSerializer,
    responses={
        200: OpenApiResponse(
            description="Код регистрации отправлен на ваш email",
            examples=[OpenApiExample("Успешная регистрация", value={"message": "Код регистрации отправлен на ваш email"})]
        ),
        400: OpenApiResponse(
            description="Ошибка валидации",
            examples=[OpenApiExample("Ошибка валидации", value={"email": ["Этот email уже используется"], "password": ["Поле обязательно"]})]
        )
    }
)
@extend_schema(tags=['Register'])
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = User.objects.create_user(email=email, password=password, is_active=False)
            code = EmailConfirmation.generate_code()
            EmailConfirmation.objects.create(user=user, code=code)

            send_mail(
                'Ваш код регистрации',
                f'Ваш код: {code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
            return Response({'message': 'Код регистрации отправлен на ваш email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================== Подтверждение регистрации ==================
@extend_schema(
    summary="Подтверждение регистрации",
    description="Подтверждение регистрации пользователя по email и коду",
    request=ConfirmRegistrationSerializer,
    responses={
        200: OpenApiResponse(
            description="Регистрация успешно подтверждена",
            examples=[OpenApiExample("Успешный ответ", value={"message": "Регистрация подтверждена", "token": "jwt_access_token"})]
        ),
        400: OpenApiResponse(
            description="Ошибка валидации",
            examples=[OpenApiExample("Ошибка валидации", value={"error": "Код истёк"})]
        )
    }
)
@extend_schema(tags=['Register'])
class ConfirmRegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ConfirmRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            try:
                user = User.objects.get(email=email)
                confirmation = EmailConfirmation.objects.get(user=user, code=code)

                if confirmation.is_expired():
                    user.delete()
                    return Response({'error': 'Срок кода истёк'}, status=status.HTTP_400_BAD_REQUEST)

                user.is_active = True
                user.save()
                confirmation.delete()

                refresh = RefreshToken.for_user(user)
                return Response({'message': 'Регистрация подтверждена', 'token': str(refresh.access_token)}, status=status.HTTP_200_OK)
            except (User.DoesNotExist, EmailConfirmation.DoesNotExist):
                return Response({'error': 'Некорректные данные'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================== Авторизация пользователя ==================
@extend_schema(
    summary="Авторизация пользователя",
    description="Авторизация пользователя по email и паролю с выдачей токена",
    request=LoginSerializer,
    responses={
        200: OpenApiResponse(
            description="Успешный вход",
            examples=[OpenApiExample("Успешный вход", value={"token": "jwt_access_token"})]
        ),
        400: OpenApiResponse(
            description="Ошибка авторизации",
            examples=[OpenApiExample("Ошибка авторизации", value={"non_field_errors": ["Неверный email или пароль"]})]
        )
    }
)
@extend_schema(tags=['Login'])
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(username=email, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)
            return Response({'non_field_errors': ['Неверный email или пароль']}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================== Запрос на сброс пароля ==================
@extend_schema(
    summary="Запрос на сброс пароля",
    description="Отправляет ссылку для сброса пароля на указанный email",
    request=RequestPasswordResetSerializer,
    responses={
        200: OpenApiResponse(
            description="Ссылка для сброса пароля отправлена",
            examples=[OpenApiExample("Успешный ответ", value={"message": "Ссылка для сброса пароля отправлена на ваш email"})]
        ),
        400: OpenApiResponse(
            description="Ошибка валидации",
            examples=[OpenApiExample("Ошибка валидации", value={"email": ["Пользователь с таким email не найден"]})]
        )
    }
)
@extend_schema(tags=['Reset-Password'])
class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        if getattr(request, 'limited', False):
            return Response({'error': 'Превышен лимит запросов'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        serializer = RequestPasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)

                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_url = f"{settings.DOMEN_URL}/api/authentication/reset-password/{uid}/{token}/"

                send_mail(
                    'Ссылка для сброса пароля',
                    f'Для сброса пароля перейдите по ссылке: {reset_url}',
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )

                return Response({'message': 'Ссылка для сброса пароля отправлена на ваш email'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'Пользователь с таким email не найден'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================== Сброс пароля ==================
@extend_schema(
    summary="Сброс пароля",
    description="Завершает процесс сброса пароля",
    request=ResetPasswordSerializer,
    responses={
        200: OpenApiResponse(
            description="Пароль успешно изменен.",
            examples=[OpenApiExample("Успешный ответ", value={"message": "Пароль успешно изменен"})]
        ),
        400: OpenApiResponse(
            description="Ошибка валидации или недействительный токен",
            examples=[OpenApiExample("Ошибка валидации или недействительный токен", value={"error": "Недействительный токен"})]
        )
    }
)
@extend_schema(tags=['Reset-Password'])
class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']

            try:
                uid = urlsafe_base64_decode(uidb64).decode()
                user = User.objects.get(pk=uid)
            except (User.DoesNotExist, ValueError, TypeError):
                return Response({'error': 'Недействительная ссылка'}, status=status.HTTP_400_BAD_REQUEST)

            if not default_token_generator.check_token(user, token):
                return Response({'error': 'Недействительный токен'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({'message': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ================== Профиль пользователя ==================
@extend_schema_view(  
    list=extend_schema(  
        summary="Получить профиль",  
        description="Возвращает профиль текущего пользователя",
        responses={200: ProfileSerializer}
    ),  
    create=extend_schema(  
        summary="Создать профиль",  
        description="Создает профиль для текущего пользователя",  
        request=ProfileSerializer,  
        responses={201: ProfileSerializer, 400: OpenApiResponse(description="Ошибка валидации: Профиль уже существует")}  
    ),  
    retrieve=extend_schema(  
        summary="Получить детали профиля",  
        description="Возвращает детальную информацию о профиле пользователя",
        responses={200: ProfileSerializer}
    ),  
    update=extend_schema(  
        summary="Обновить профиль",  
        description="Обновляет информацию о текущем пользователе",
        request=ProfileSerializer,  
        responses={200: ProfileSerializer, 400: OpenApiResponse(description="Ошибка валидации")}  
    ),  
    partial_update=extend_schema(  
        summary="Частичное обновление профиля",  
        description="Частично обновляет профиль текущего пользователя",
        request=ProfileSerializer,
        responses={200: ProfileSerializer, 400: OpenApiResponse(description="Ошибка валидации")}
    )  
)
@extend_schema(tags=['Profile'])
class ProfileViewSet(viewsets.ModelViewSet):  
    queryset = Profile.objects.all()  
    serializer_class = ProfileSerializer  
    permission_classes = [IsAuthenticated]  

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)  
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
