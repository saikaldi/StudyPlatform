from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import (
    TestCategory,
    Test,
    TestContent,
    TestFullDescription,
    UserAnswer,
    UserStatistic,
    SubjectCategory,
    OkupTushunuu,
    OkupTushunuuQuestion,
)
from .serializers import (
    TestCategorySerializer,
    TestSerializer,
    TestContentSerializer,
    TestFullDescriptionSerializer,
    UserAnswerSerializer,
    UserStatisticSerializer,
    SubjectCategorySerializer,
    OkupTushunuuSerializer,
    OkupTushunuuQuestionSerializer,
    OkupTushunuuTextSerializer,
)
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend


@extend_schema(
    summary="Создание и получение категорий тестов",
    description="Этот эндпоинт позволяет создавать и получать категории тестов",
    request=TestCategorySerializer,
    responses={
        200: TestCategorySerializer,
        201: OpenApiResponse(description="Категория теста успешно создана"),
    },
)
@extend_schema(tags=["Test-Category: Негизки тест, Тесты предметов"])
class TestCategoryViewSet(viewsets.ModelViewSet):
    queryset = TestCategory.objects.all()
    serializer_class = TestCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TestCategoryFilter


@extend_schema(
    summary="Создание и получение категорий предметов",
    description="Этот эндпоинт позволяет создавать и получать категории предметов",
    request=SubjectCategory,
    responses={
        200: SubjectCategorySerializer,
        201: OpenApiResponse(description="Категория Предмета успешно создана"),
    },
)
@extend_schema(tags=["Test-Subject-Category: Математика, Кыргыз тили"])
class SubjectCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubjectCategory.objects.all()
    serializer_class = SubjectCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubjectCategoryFilter


@extend_schema(
    summary="Создание и получение тестов",
    description="Этот эндпоинт позволяет создавать и получать тесты",
    request=TestSerializer,
    responses={
        200: TestSerializer,
        201: OpenApiResponse(description="Тест успешно создан"),
    },
)
@extend_schema(tags=["Test: Математика 1 болум, Математика 2 болум"])
class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TestFilter


@extend_schema(
    summary="Создание и получение данных теста",
    description="Этот эндпоинт позволяет создавать и получать данные теста",
    request=TestContentSerializer,
    responses={
        200: TestContentSerializer,
        201: OpenApiResponse(description="Данные теста успешно созданы"),
    },
)
@extend_schema(tags=["Test-Content: Вопросы тестов"])
class TestContentViewSet(viewsets.ModelViewSet):
    queryset = TestContent.objects.all()
    serializer_class = TestContentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TestContentFilter


@extend_schema(
    summary="Создание и получение полного описания тестов",
    description="Этот эндпоинт позволяет создавать и получать полное описание тестов",
    request=TestFullDescriptionSerializer,
    responses={
        200: TestFullDescriptionSerializer,
        201: OpenApiResponse(description="Описание теста успешно создано"),
    },
)
@extend_schema(tags=["Test-Description: Описание тестов"])
class TestFullDescriptionViewSet(viewsets.ModelViewSet):
    queryset = TestFullDescription.objects.all()
    serializer_class = TestFullDescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TestFullDescriptionFilter


# @extend_schema(
#     summary="Создание и получение инструкций для тестов",
#     description="Этот эндпоинт позволяет создавать и получать инструкции для тестов",
#     request=TestInstructionSerializer,
#     responses={
#         200: TestInstructionSerializer,
#         201: OpenApiResponse(description="Инструкция успешно создана"),
#     },
# )
# @extend_schema(tags=["Test-Instructions"])
# class TestInstructionViewSet(viewsets.ModelViewSet):
#     queryset = TestInstruction.objects.all()
#     serializer_class = TestInstructionSerializer
#     permission_classes = [permissions.IsAuthenticated]


# @extend_schema(
#     summary="Создание и получение дополнительных инструкций для тестов",
#     description="Этот эндпоинт позволяет создавать и получать дополнительные инструкции для тестов",
#     request=AdditionalInstructionSerializer,
#     responses={
#         200: AdditionalInstructionSerializer,
#         201: OpenApiResponse(description="Дополнительная инструкция успешно создана"),
#     }
# )
# @extend_schema(tags=['Additional-Instructions'])
# class AdditionalInstructionViewSet(viewsets.ModelViewSet):
#     queryset = AdditionalInstruction.objects.all()
#     serializer_class = AdditionalInstructionSerializer
#     permission_classes = [permissions.IsAuthenticated]


@extend_schema(tags=["User Answer for Test"])
class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserAnswerFilter

    @extend_schema(
        summary="Создание ответа пользователя на тест",
        description=(
            "Этот эндпоинт позволяет пользователю отправить свой ответ на тест"
            "Перед созданием ответа проверяется, был ли уже отправлен ответ на данный контент теста"
            "Если ответ уже существует, будет возвращена ошибка"
            "Если тест не является бесплатным, также будет возвращена ошибка"
        ),
        request=UserAnswerSerializer,
        responses={
            201: OpenApiResponse(description="Ответ пользователя успешно создан"),
            400: OpenApiResponse(description="Пользователь уже отвечал на этот тест"),
            404: OpenApiResponse(description="Нет доступных бесплатных тестов"),
        },
    )
    def create(self, request, *args, **kwargs):
        user = request.user
        test_content_id = request.data.get("test_content")
        user_answer = request.data.get("answer_vars")

        if not Test.objects.filter(first_test=True).exists():
            return Response(
                {"detail": "Нет доступных бесплатных тестов"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if UserAnswer.objects.filter(user=user, test_content=test_content_id).exists():
            return Response(
                {"detail": "Пользователь уже отвечал на этот контент теста"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        test_content = TestContent.objects.get(id=test_content_id)
        if not test_content:
            return Response(
                {"detail": "Контент теста не найден"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        statistics, created = UserStatistic.objects.get_or_create(
            user=user, test=test_content.test
        )
        if user_answer == test_content.true_answer:
            statistics.true_answer_count += 1
        else:
            statistics.false_answer_count += 1
        statistics.save()

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(
    summary="Создание и получение количества ответов пользователей на тесты",
    description="Этот эндпоинт позволяет создавать и получать количество правильных и неправильных ответов пользователей на тесты",
    request=UserStatisticSerializer,
    responses={
        200: UserStatisticSerializer,
        201: OpenApiResponse(description="Счёт ответов пользователя успешно сохранён"),
    },
)
@extend_schema(tags=["User-Statistics: Cтатистика студентов"])
class UserStatisticViewSet(viewsets.ModelViewSet):
    queryset = UserStatistic.objects.all()
    serializer_class = UserStatisticSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserStatisticFilter


@extend_schema(tags=["OkupTushunuu Tests: Тесты - Чтение и понимание"])
class OkupTushunuuViewSet(viewsets.ModelViewSet):
    queryset = OkupTushunuu.objects.all()
    serializer_class = OkupTushunuuSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OkupTushunuuFilter


@extend_schema(tags=["OkupTushunuu Text: Текст - Чтение и понимание"])
class OkupTushunuuTextViewSet(viewsets.ModelViewSet):
    queryset = OkupTushunuuText.objects.all()
    serializer_class = OkupTushunuuTextSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OkupTushunuuTextFilter


@extend_schema(tags=["OkupTushunuu Questions: Вопросы - Чтение и понимание"])
class OkupTushunuuQuestionViewSet(viewsets.ModelViewSet):
    queryset = OkupTushunuuQuestion.objects.all()
    serializer_class = OkupTushunuuQuestionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OkupTushunuuQuestionFilter
