from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import MockAssessmentTest, MockAssessmentTestContent, MockAssessmentTestFullDescription, MockAssessmentTestInstruction, MockAssessmentTest, MockAssessmentAnswer, MockAssessmentUserStatistic, MockAssessmentUser
from .serializers import MockAssessmentTestSerializer, MockAssessmentTestContentSerializer, MockAssessmentTestFullDescriptionSerializer, MockAssessmentTestInstructionSerializer, MockAssessmentTestSerializer, MockAssessmentAnswerSerializer, UserStatisticSerializer, MockAssessmentAnswerCreateSerializer, MockAssessmentUserSerializer
from django_filters.rest_framework import DjangoFilterBackend
# from .filters import *


@extend_schema(
    tags=['MockAssessmentTests'],
    summary="Управление тестами",
    description="Эндпоинт для создания, чтения, обновления и удаления тестов",
    request=MockAssessmentTestSerializer,
    responses={
        200: MockAssessmentTestSerializer,
        201: OpenApiResponse(description="Тест успешно создан"),
    },
)
class MockAssessmentTestViewSet(viewsets.ModelViewSet):
    queryset = MockAssessmentTest.objects.all()
    serializer_class = MockAssessmentTestSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = TestFilter

@extend_schema(
    tags=['MockAssessmentTestContent'],
    summary="Управление содержанием тестов",
    description="Эндпоинт для работы с вопросами тестов",
    request=MockAssessmentTestContentSerializer,
    responses={
        200: MockAssessmentTestContentSerializer,
        201: OpenApiResponse(description="Вопрос теста успешно создан"),
    },
)
class MockAssessmentTestContentViewSet(viewsets.ModelViewSet):
    queryset = MockAssessmentTestContent.objects.all()
    serializer_class = MockAssessmentTestContentSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = TestContentFilter

@extend_schema(
    tags=['MockAssessmentTestDescriptions'],
    summary="Управление описаниями тестов",
    description="Эндпоинт для создания, чтения, обновления и удаления полных описаний тестов",
    request=MockAssessmentTestFullDescriptionSerializer,
    responses={
        200: MockAssessmentTestFullDescriptionSerializer,
        201: OpenApiResponse(description="Описание теста успешно создано"),
    },
)
class MockAssessmentTestFullDescriptionViewSet(viewsets.ModelViewSet):
    queryset = MockAssessmentTestFullDescription.objects.all()
    serializer_class = MockAssessmentTestFullDescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = TestFullDescriptionFilter

@extend_schema(
    tags=['TestInstructions'],
    summary="Управление инструкциями для тестов",
    description="Эндпоинт для работы с инструкциями тестов",
    request=MockAssessmentTestInstructionSerializer,
    responses={
        200: MockAssessmentTestInstructionSerializer,
        201: OpenApiResponse(description="Инструкция успешно создана"),
    },
)
class MockAssessmentTestInstructionViewSet(viewsets.ModelViewSet):
    queryset = MockAssessmentTestInstruction.objects.all()
    serializer_class = MockAssessmentTestInstructionSerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema(
    tags=['MockAssessment'],
    summary="Управление пользователями для пробных тестов",
    description="Эндпоинт для работы с пользователями, которые проходят тесты",
    request=MockAssessmentUserSerializer,
    responses={
        200: MockAssessmentUserSerializer,
        201: OpenApiResponse(description="Запись пользователя успешно создана"),
    },
)
class MockAssessmentUserViewSet(viewsets.ModelViewSet):
    queryset = MockAssessmentUser.objects.all()
    serializer_class = MockAssessmentUserSerializer
    permission_classes = [permissions.AllowAny]  # Разрешение для всех, так как регистрация не требуется
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = MockAssessmentTestFilter

@extend_schema(
    tags=['MockAssessment'],
    summary="Управление ответами на пробные тесты",
    description="Эндпоинт для отправки и получения ответов пользователей на тесты",
    request=MockAssessmentAnswerSerializer,
    responses={
        200: MockAssessmentAnswerSerializer,
        201: OpenApiResponse(description="Ответ на тест успешно сохранён"),
    },
)
class MockAssessmentAnswerViewSet(viewsets.ModelViewSet):
    queryset = MockAssessmentAnswer.objects.all()
    serializer_class = MockAssessmentAnswerSerializer
    permission_classes = [permissions.AllowAny]
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = MockAssessmentAnswerFilter

    def create(self, request, *args, **kwargs):
        # Проверка существования пользователя по номеру телефона
        phone_number = request.data.get('phone_number')
        user_data, created = MockAssessmentTest.objects.get_or_create(
            phone_number=phone_number,
            defaults={
                'first_name': request.data.get('first_name'),
                'last_name': request.data.get('last_name')
            }
        )

        # Убедимся, что данные пользователя из запроса совпадают или обновим их
        if not created:
            user_data.first_name = request.data.get('first_name', user_data.first_name)
            user_data.last_name = request.data.get('last_name', user_data.last_name)
            user_data.save()

        # Создание ответа
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        test_content = TestContent.objects.get(id=request.data.get('test_content_id'))
        answer_vars = request.data.get('answer_vars')
        is_correct = answer_vars == test_content.true_answer

        # Обновление статистики пользователя
        user_stat, created = UserStatistic.objects.get_or_create(
            test=test_content.test, 
            user=user_data
        )
        if is_correct:
            user_stat.true_answer_count += 1
        else:
            user_stat.false_answer_count += 1
        user_stat.save()

        # Сохранение ответа
        serializer.save(mock_test=user_data, test_content=test_content, is_correct=is_correct)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@extend_schema(
    tags=['MockAssessmentUserStatistics'],
    summary="Управление статистикой ответов пользователей",
    description="Эндпоинт для отслеживания статистики ответов пользователей",
    request=UserStatisticSerializer,
    responses={
        200: UserStatisticSerializer,
        201: OpenApiResponse(description="Статистика ответов успешно обновлена"),
    },
)
class MockAssessmentUserStatisticViewSet(viewsets.ModelViewSet):
    queryset = MockAssessmentUserStatistic.objects.all()
    serializer_class = UserStatisticSerializer
    permission_classes = [permissions.IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = UserStatisticFilter

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

@extend_schema(
    request=MockAssessmentAnswerCreateSerializer,
    responses={201: MockAssessmentAnswerCreateSerializer},
    methods=["POST"],
    description="Отправка ответа на вопрос теста",
    examples=[
        OpenApiExample(
            'Пример запроса',
            value={
                'var': 'Б',
                'content': 12,
                'phone_number': '+996700123456',
                'first_name': 'Анна',
                'last_name': 'Смирнова'
            },
            status_codes=['201'],
            request_only=True
        )
    ]
)
@api_view(['POST'])
def submit_answer(request, test_id):
    # Получаем тест и вопрос
    test = get_object_or_404(MockAssessmentTest, id=test_id)
    question_id = request.data.get('question_id')
    user_answer = request.data.get('answer', '').lower()  # Приводим к нижнему регистру
    
    # Проверяем существование вопроса
    try:
        question = MockAssessmentTestContent.objects.get(id=question_id, test=test)
    except MockAssessmentTestContent.DoesNotExist:
        return Response(
            {"error": "Question not found in this test"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Проверяем валидность ответа
    valid_answers = {'а', 'б', 'в', 'г', 'д'}
    if user_answer not in valid_answers:
        return Response(
            {"error": "Invalid answer. Use А-Д"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Сохраняем ответ
    answer, created = MockAssessmentAnswer.objects.update_or_create(
        mock_test=request.session,
        test_content=question,
        defaults={
            'answer_vars': user_answer,
            'is_correct': user_answer == question.true_answer
        }
    )

    return Response({
        "status": "Answer saved",
        "correct": answer.is_correct,
        "correct_answer": question.true_answer
    }, status=status.HTTP_201_CREATED)

# views.py
@api_view(['GET'])
def get_mock_results(request, session_id):
    session = get_object_or_404(MockAssessmentTest, pk=session_id)
    answers = MockAssessmentAnswer.objects.filter(mock_test=session)
    
    results = {
        "total_questions": answers.count(),
        "correct_answers": answers.filter(is_correct=True).count(),
        "details": [
            {
                "question_id": answer.test_content.id,
                "correct_answer": answer.test_content.true_answer,
                "user_answer": answer.answer_vars,
                "is_correct": answer.is_correct
            } for answer in answers
        ]
    }
    
    return Response(results)
