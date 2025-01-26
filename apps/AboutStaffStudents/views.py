from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, BasePermission, AllowAny
from .models import Subject, Graduate, Teacher, Feedback
from .serializers import SubjectSerializer, GraduateSerializer, TeacherSerializer, FeedbackSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from rest_framework import status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *


class CanViewGraduates(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user.is_authenticated and request.user.user_status in ["Менеджер", "Админ", "Учитель"]

def check_user_status(request):
    return request.user.is_status_approved and request.user.user_status in ["Менеджер", "Админ", "Учитель"]

@extend_schema(
    summary="Предметы",
    description="API для управления предметами",
    tags=['Subjects'],
)
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubjectFilter

    @extend_schema(
        summary="Создать предмет",
        description="Создает новый предмет в системе",
        request=SubjectSerializer,
        responses={
            201: OpenApiResponse(description='Предмет успешно создан', examples=[
                OpenApiExample(
                    'Пример ответа',
                    value={'id': 1, 'name': 'Математика', 'description': 'Основы математики'},
                    response_only=True
                )
            ]),
            400: OpenApiResponse(description='Ошибка валидации данных'),
            403: OpenApiResponse(description='Доступ запрещен'),
        }
    )
    def create(self, request, *args, **kwargs):
        if check_user_status(request):
            return super().create(request, *args, **kwargs)
        else:
            return Response({'message': 'У вас нет прав для этого действия'}, status=status.HTTP_403_FORBIDDEN)
    
    @extend_schema(
        summary="Обновить предмет",
        description="Обновляет существующий предмет",
        request=SubjectSerializer,
        responses={
            200: OpenApiResponse(description='Предмет успешно обновлен'),
            400: OpenApiResponse(description='Ошибка валидации данных'),
            403: OpenApiResponse(description='Доступ запрещен'),
            404: OpenApiResponse(description='Предмет не найден'),
        }
    )
    def update(self, request, *args, **kwargs):
        if check_user_status(request):
            return super().update(request, *args, **kwargs)
        else:
            return Response({'message': 'У вас нет прав для этого действия'}, status=status.HTTP_403_FORBIDDEN)
    
    @extend_schema(
        summary="Удалить предмет",
        description="Удаляет предмет из системы",
        responses={
            204: OpenApiResponse(description='Предмет успешно удален'),
            403: OpenApiResponse(description='Доступ запрещен'),
            404: OpenApiResponse(description='Предмет не найден'),
        }
    )
    def destroy(self, request, *args, **kwargs):
        if check_user_status(request):
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({'message': 'У вас нет прав для этого действия'}, status=status.HTTP_403_FORBIDDEN)
    
    @extend_schema(
        summary="Частично обновить предмет",
        description="Частично обновляет существующий предмет",
        request=SubjectSerializer,
        responses={
            200: OpenApiResponse(description='Предмет успешно частично обновлен'),
            400: OpenApiResponse(description='Ошибка валидации данных'),
            403: OpenApiResponse(description='Доступ запрещен'),
            404: OpenApiResponse(description='Предмет не найден'),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        if check_user_status(request):
            return super().partial_update(request, *args, **kwargs)
        else:
            return Response({'message': 'У вас нет прав для этого действия'}, status=status.HTTP_403_FORBIDDEN)

@extend_schema(
    summary="Выпускники",
    description="API для управления информацией о выпускниках",
    tags=['Graduate'],
)
class GraduateViewSet(viewsets.ModelViewSet):
    queryset = Graduate.objects.all()
    serializer_class = GraduateSerializer
    permission_classes = [CanViewGraduates]
    filter_backends = [DjangoFilterBackend]
    filterset_class = GraduateFilter

    @extend_schema(
        summary="Создать выпускника",
        description="Создает нового выпускника в системе",
        request=GraduateSerializer,
        responses={
            201: OpenApiResponse(description='Выпускник успешно создан'),
            400: OpenApiResponse(description='Ошибка валидации данных'),
            403: OpenApiResponse(description='Доступ запрещен'),
        }
    )
    def create(self, request, *args, **kwargs):
        if check_user_status(request):
            return super().create(request, *args, **kwargs)
        else:
            return Response({'message': 'У вас нет прав для этого действия'}, status=status.HTTP_403_FORBIDDEN)
    
    @extend_schema(
        summary="Обновить выпускника",
        description="Обновляет информацию о существующем выпускнике",
        request=GraduateSerializer,
        responses={
            200: OpenApiResponse(description='Выпускник успешно обновлен'),
            400: OpenApiResponse(description='Ошибка валидации данных'),
            403: OpenApiResponse(description='Доступ запрещен'),
            404: OpenApiResponse(description='Выпускник не найден'),
        }
    )
    def update(self, request, *args, **kwargs):
        if check_user_status(request):
            return super().update(request, *args, **kwargs)
        else:
            return Response({'message': 'У вас нет прав для этого действия'}, status=status.HTTP_403_FORBIDDEN)
    
    @extend_schema(
        summary="Удалить выпускника",
        description="Удаляет выпускника из системы",
        responses={
            204: OpenApiResponse(description='Выпускник успешно удален'),
            403: OpenApiResponse(description='Доступ запрещен'),
            404: OpenApiResponse(description='Выпускник не найден'),
        }
    )
    def destroy(self, request, *args, **kwargs):
        if check_user_status(request):
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({'message': 'У вас нет прав для этого действия'}, status=status.HTTP_403_FORBIDDEN)
    
    @extend_schema(
        summary="Частично обновить выпускника",
        description="Частично обновляет информацию о существующем выпускнике",
        request=GraduateSerializer,
        responses={
            200: OpenApiResponse(description='Выпускник успешно частично обновлен'),
            400: OpenApiResponse(description='Ошибка валидации данных'),
            403: OpenApiResponse(description='Доступ запрещен'),
            404: OpenApiResponse(description='Выпускник не найден'),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        if check_user_status(request):
            return super().partial_update(request, *args, **kwargs)
        else:
            return Response({'message': 'У вас нет прав для этого действия'}, status=status.HTTP_403_FORBIDDEN)

@extend_schema(
    summary="Преподаватели",
    description="API для управления информацией о преподавателях",
    tags=['Teachers'],
)
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [CanViewGraduates]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TeacherFilter

    @extend_schema(
        summary="Создать преподавателя",
        description="Создает нового преподавателя в системе",
        request=TeacherSerializer,
        responses={
            201: OpenApiResponse(description='Преподаватель успешно создан'),
            400: OpenApiResponse(description='Ошибка валидации данных'),
            403: OpenApiResponse(description='Доступ запрещен'),
        }
    )
    def create(self, request, *args, **kwargs):
        if check_user_status(request):
            return super().create(request, *args, **kwargs)
        else:
            return Response({'message': 'У вас нет прав для этого действия'}, status=status.HTTP_403_FORBIDDEN)
    
    @extend_schema(
        summary="Обновить преподавателя",
        description="Обновляет информацию о существующем преподавателе",
        request=TeacherSerializer,
        responses={
            200: OpenApiResponse(description='Преподаватель успешно обновлен'),
            400: OpenApiResponse(description='Ошибка валидации данных'),
            403: OpenApiResponse(description='Доступ запрещен'),
            404: OpenApiResponse(description='Преподаватель не найден'),
        }
    )
    def update(self, request, *args, **kwargs):
        if check_user_status(request):
            return super().update(request, *args, **kwargs)
        else:
            return Response({'message': 'У вас нет прав для этого действия'}, status=status.HTTP_403_FORBIDDEN)
    
    @extend_schema(
        summary="Удалить преподавателя",
        description="Удаляет преподавателя из системы",
        responses={
            204: OpenApiResponse(description='Преподаватель успешно удален'),
            403: OpenApiResponse(description='Доступ запрещен'),
            404: OpenApiResponse(description='Преподаватель не найден'),
        }
    )
    def destroy(self, request, *args, **kwargs):
        if check_user_status(request):
            return super().destroy(request, *args, **kwargs)
        else:
            return Response({'message': 'У вас нет прав для этого действия'}, status=status.HTTP_403_FORBIDDEN)
    
    @extend_schema(
        summary="Частично обновить преподавателя",
        description="Частично обновляет информацию о существующем преподавателе",
        request=TeacherSerializer,
        responses={
            200: OpenApiResponse(description='Преподаватель успешно частично обновлен'),
            400: OpenApiResponse(description='Ошибка валидации данных'),
            403: OpenApiResponse(description='Доступ запрещен'),
            404: OpenApiResponse(description='Преподаватель не найден'),
        }
    )
    def partial_update(self, request, *args, **kwargs):
        if check_user_status(request):
            return super().partial_update(request, *args, **kwargs)
        else:
            return Response({'message': 'У вас нет прав для этого действия'}, status=status.HTTP_403_FORBIDDEN)

@extend_schema(
    summary="Обратная связь",
    description="API для создания обратной связи",
    tags=['Feedback'],
)
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FeedbackFilter
