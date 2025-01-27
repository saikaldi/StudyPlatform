from django.core.mail import send_mail
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from .models import EmailConfirmation, Profile, MockAssessmentTest
from .serializers import ProfileSerializer, RegisterSerializer, ConfirmRegistrationSerializer, LoginSerializer, RequestPasswordResetSerializer, ResetPasswordSerializer, MockAssessmentTestSerializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample, OpenApiParameter
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *

User = get_user_model()


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
            user_status = serializer.validated_data['user_status']
            first_name = serializer.validated_data['first_name']
            last_name = serializer.validated_data['last_name']

            with transaction.atomic():
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    is_active=False,
                    user_status=user_status,
                    first_name=first_name,
                    last_name=last_name
                )

                if user_status != 'Студент':
                    user.is_status_approved = False
                    user.save()

                    send_mail(
                        'Новый пользователь на подтверждение',
                        f'Пользователь {user.email} выбрал статус {user_status} \nПожалуйста, рассмотрите его/ее запрос',
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.ADMIN_EMAIL],
                    )

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
    filter_backends = [DjangoFilterBackend]
    filterset_class = EmailConfirmationFilter

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        code = request.data.get('code')

        try:
            user = User.objects.get(email=email)
            confirmation = EmailConfirmation.objects.get(user=user, code=code)
        except (User.DoesNotExist, EmailConfirmation.DoesNotExist):
            return Response({'message': 'Неверный код или email'}, status=status.HTTP_400_BAD_REQUEST)

        if confirmation.is_used:
            return Response({'message': 'Этот код уже был использован'}, status=status.HTTP_400_BAD_REQUEST)

        if confirmation.is_expired():
            if not confirmation.is_used:
                user.delete()
                return Response({'message': 'Код подтверждения истек, запросите код повторно'}, status=status.HTTP_400_BAD_REQUEST)

        confirmation.is_used = True
        confirmation.save()

        user.is_active = True
        user.save()

        if user.user_status != 'Студент':
            user.is_approved_by_admin = False
            user.save()

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        return Response({'message': 'Каттоо эсеби ийгиликтүү ырасталды жана жандырылды', 'token': token}, status=status.HTTP_200_OK)

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
            description="Пароль успешно изменен",
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
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProfileFilter

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)  
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema(
    summary="Подтверждение пользователя администратором",
    description="Администратор подтверждает аккаунт пользователя, обновляет его статус и отправляет подтверждение на email",
    request={
        'application/json': OpenApiResponse(
            description="Данные запроса",
            examples=[
                OpenApiExample(
                    'Пример запроса',
                    value={'email': 'user@example.com'}
                )
            ]
        )
    },
    responses={
        200: OpenApiResponse(
            description="Пользователь успешно подтвержден",
            examples=[OpenApiExample(
                'Успешный запрос',
                value={'message': 'Пользователь подтвержден'}
            )]
        ),
        400: OpenApiResponse(
            description="Ошибка: Аккаунт уже подтвержден",
            examples=[OpenApiExample(
                'Ошибка подтверждения',
                value={'message': 'Аккаунт пользователя уже был подтвержден'}
            )]
        ),
        404: OpenApiResponse(
            description="Ошибка: Пользователь не найден",
            examples=[OpenApiExample(
                'Пользователь не найден',
                value={'message': 'Пользователь с таким email не найден'}
            )]
        )
    }
)
@extend_schema(tags=['admin-confirm-user'])
class AdminConfirmUserView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'Пользователь с таким email не найден'}, status=status.HTTP_404_NOT_FOUND)

        if user.is_status_approved is True:
            return Response({'message': 'Аккаунт пользователя уже был подтвержден'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_status_approved = True
        if user.user_status == 'Админ':
            user.is_superuser = True
            user.is_staff = True
            user.user_status = "Админ"
        user.save()

        self.send_confirmation_email(user)

        return Response({'message': 'Пользователь подтвержден'}, status=status.HTTP_200_OK)

    def send_confirmation_email(self, user):
        subject = 'Ваш аккаунт подтвержден'
        message = f'''
            Здравствуйте, {user.email}!

            Ваш аккаунт был подтвержден администратором
            Ваш текущий статус: {user.user_status}

            Поздравляем с успешным подтверждением!
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )

@extend_schema(
    description="Модель для пробной записи на оценочный тест",
    responses={200: MockAssessmentTestSerializer},
)
@extend_schema(tags=['mock-assessment-tests'])
class MockAssessmentTestViewSet(viewsets.ModelViewSet):
    queryset = MockAssessmentTest.objects.all()
    serializer_class = MockAssessmentTestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MockAssessmentTestFilter
