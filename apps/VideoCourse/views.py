from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import CategoryVideo, Video, TestContent, UserStatistic, UserAnswer, SubjectCategory,Category
from .serializers import CategoryVideoSerializer, VideoSerializer, TestContentSerializer, UserStatisticSerializer, UserAnswerSerializer, SubjectCategorySerializer, CategorySerializer
from .filters import *
from django_filters.rest_framework import DjangoFilterBackend

User = get_user_model()


def check_paid_access(user, video):
    if video.is_paid and getattr(user, "paid", "Не оплачено") == "Не оплачено":
        return Response(
            {"error": "Доступ запрещен: Контент платный"},
            status=status.HTTP_403_FORBIDDEN,
        )
    return None

@extend_schema(
    summary="Создание и получение категорий видео",
    description="Этот эндпоинт позволяет создавать и получать категории видео",
    request=CategoryVideoSerializer,
    responses={
        200: CategoryVideoSerializer,
        201: OpenApiResponse(description="Категория видео успешно создана"),
    },
)
@extend_schema(tags=["Video-Category: Негизки тест, Предметтик тест"])
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

@extend_schema(
    summary="Создание и получение категорий предметов",
    description="Этот эндпоинт позволяет создавать и получать категории предметов",
    request=SubjectCategorySerializer,
    responses={
        200: SubjectCategorySerializer,
        201: OpenApiResponse(description="Категория Предмета успешно создана"),
    },
)
@extend_schema(tags=["Video-Category: Математика, Кыргыз тил"])
class CategoryVideoViewSet(viewsets.ModelViewSet):
    queryset = CategoryVideo.objects.all()
    serializer_class = CategoryVideoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryVideoFilter

@extend_schema(
    summary="Создание и получение категорий предметов",
    description="Этот эндпоинт позволяет создавать и получать категории предметов",
    request=SubjectCategorySerializer,
    responses={
        200: SubjectCategorySerializer,
        201: OpenApiResponse(description="Категория Предмета успешно создана"),
    },
)
@extend_schema(tags=["Video-Subject-Category: Математика 1 болум, математика 2 болум"])
class SubjectCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubjectCategory.objects.all()
    serializer_class = SubjectCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = SubjectCategoryFilter

@extend_schema(tags=["Video-Cources"])
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = VideoFilter

    @extend_schema(
        summary="Проверка доступа к видео",
        description="Проверяет, может ли пользователь получить доступ к видео на основе его статистики и предыдущих курсов",
        responses={
            200: OpenApiResponse(
                description="Успешный доступ к видео",
                examples=[
                    OpenApiExample(
                        "Доступ разрешен",
                        value={"Good Response": "Вы успешно прошли этот курс"},
                    )
                ],
            ),
            403: OpenApiResponse(
                description="Доступ запрещен из-за недостаточной успеваемости",
                examples=[
                    OpenApiExample(
                        "Доступ запрещен",
                        value={
                            "error": "Вы прошли предыдущий курс на < 80%. Чтобы получить доступ к этому тесту, пройдите предыдущий курс на > 80%"
                        },
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Статистика не найдена",
                examples=[
                    OpenApiExample(
                        "Статистика не найдена",
                        value={"error": "Вы еще не проходили тесты этого курса"},
                    )
                ],
            ),
        },
    )
    @action(detail=True, methods=["get"], permission_classes=[IsAuthenticated])
    def check_access(self, request, pk=None):
        video = self.get_object()
        user = request.user

        paid_access_error = check_paid_access(user, video)
        if paid_access_error:
            return paid_access_error

        try:
            statistic = UserStatistic.objects.get(video=video, user=user)

            video_pre_course = (
                UserStatistic.objects.filter(
                    video__video_category=video.video_category,
                    video__video_order__lt=video.video_order,
                    user=user,
                )
                .order_by("-video__video_order")
                .first()
            )

            video_first_course = (
                Video.objects.filter(video_category=video.video_category)
                .order_by("video_order")
                .first()
            )

            def can_access_next_video(
                statistic, video_course, video_pre_course, video_first_course
            ):
                if (
                    video_pre_course is not None
                    and video_pre_course.video.video_order
                    > video_first_course.video_order
                ):
                    if statistic.accuracy_percentage >= 80:
                        return (
                            video_course
                            > statistic.true_answer_count + statistic.false_answer_count
                        )
                return False

            def is_first_course(video_pre_course, video_first_course):
                return (
                    video_pre_course is None
                    or video_pre_course.video.video_order
                    == video_first_course.video_order
                )

            video_course = TestContent.objects.filter(video=video).count()

            if can_access_next_video(
                statistic, video_course, video_pre_course, video_first_course
            ):
                return Response(
                    {"Good Response": "Вы успешно прошли этот курс"},
                    status=status.HTTP_200_OK,
                )
            elif is_first_course(video_pre_course, video_first_course):
                return Response(
                    {"Good Response": "Вы можете проходить тест дальше"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "error": "Вы прошли предыдущий курс на < 80%. Чтобы получить доступ к этому тесту, пройдите предыдущий курс на > 80%"
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        except UserStatistic.DoesNotExist:
            return Response(
                {"error": "Вы еще не проходили тесты этого курса"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(
        summary="Сброс всех тестов для видео",
        description="Удаляет все ответы и статистику пользователя для конкретного видео",
        responses={
            200: OpenApiResponse(
                description="Тесты успешно сброшены",
                examples=[
                    OpenApiExample(
                        "Сброс тестов",
                        value={
                            "message": "Все ответы и статистика для видео 'Example Video' сброшены"
                        },
                    )
                ],
            ),
            401: OpenApiResponse(
                description="Пользователь не аутентифицирован",
                examples=[
                    OpenApiExample(
                        "Неавторизованный доступ",
                        value={"error": "Необходимо войти в систему"},
                    )
                ],
            ),
        },
    )
    @action(detail=True, methods=["POST"])
    def reset_all_tests(self, request, pk=None):
        user = request.user
        video = self.get_object()

        if not user.is_authenticated:
            return Response(
                {"error": "Необходимо войти в систему"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        UserAnswer.objects.filter(user=user, test_content__video=video).delete()

        UserStatistic.objects.filter(user=user, video=video).delete()

        return Response(
            {
                "message": f'Все ответы и статистика для видео "{video.subject_name}" сброшены'
            }
        )

@extend_schema(tags=["Video-Test-Content: Тесты видео уроков"])
class TestContentViewSet(viewsets.ModelViewSet):
    queryset = TestContent.objects.all()
    serializer_class = TestContentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TestContentFilter

    @extend_schema(
        summary="Отправка ответа на тест",
        description="Отправляет ответ пользователя на тестовый вопрос",
        request={
            "answer": OpenApiTypes.STR,
        },
        responses={
            200: OpenApiResponse(
                description="Ответ принят",
                examples=[
                    OpenApiExample(
                        "Ответ принят",
                        value={"message": "Ответ принят", "correct": True},
                    )
                ],
            ),
            400: OpenApiResponse(
                description="Ошибки валидации или доступа",
                examples=[
                    OpenApiExample(
                        "Неверный формат ответа",
                        value={"error": "Неверный формат ответа"},
                    ),
                    OpenApiExample(
                        "Повторный ответ",
                        value={"error": "Вы уже ответили на этот вопрос"},
                    ),
                ],
            ),
            403: OpenApiResponse(
                description="Доступ запрещен",
                examples=[
                    OpenApiExample(
                        "Доступ запрещен",
                        value={
                            "error": "Вы не можете ответить на этот вопрос, так как не прошли предыдущий курс на 80% или выше"
                        },
                    )
                ],
            ),
        },
    )
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def submit_answer(self, request, pk=None):
        test_content = self.get_object()
        user = request.user
        video = test_content.video

        if Video.objects.get(id=video.id).is_paid:
            paid_access_error = check_paid_access(user, video)
            if paid_access_error:
                return paid_access_error

        answer = request.data.get("answer")
        if answer not in ["a", "b", "c", "d"]:
            return Response(
                {"error": "Неверный формат ответа"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            current_video_order = video.video_order
            previous_videos = Video.objects.filter(
                video_category=video.video_category, video_order__lt=current_video_order
            ).order_by("-video_order")

            if previous_videos.exists():
                last_video_stat = UserStatistic.objects.get(
                    video=previous_videos.first(), user=user
                )
                if last_video_stat.accuracy_percentage < 80:
                    return Response(
                        {
                            "error": "Вы не можете ответить на этот вопрос, так как не прошли предыдущий курс на 80% или выше"
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

            if UserAnswer.objects.filter(test_content=test_content, user=user).exists():
                return Response(
                    {"error": "Вы уже ответили на этот вопрос"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            correct = answer == test_content.true_answer
            UserAnswer.objects.create(
                test_content=test_content, user=user, answer_vars=answer
            )

            stat, created = UserStatistic.objects.get_or_create(video=video, user=user)
            if correct:
                stat.true_answer_count += 1
            else:
                stat.false_answer_count += 1
            stat.save()

            return Response({"message": "Ответ принят", "correct": correct})

        except UserStatistic.DoesNotExist:
            return Response(
                {"error": "Статистика пользователя для этого видео не найдена"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @extend_schema(
        summary="Сброс теста для конкретного вопроса",
        description="Удаляет ответ пользователя на конкретный вопрос и обновляет статистику",
        responses={
            200: OpenApiResponse(
                description="Тест сброшен",
                examples=[
                    OpenApiExample(
                        "Тест сброшен",
                        value={"message": "Тест сброшен для этого вопроса"},
                    )
                ],
            )
        },
    )
    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def reset_test(self, request, pk=None):
        test_content = self.get_object()
        user = request.user

        paid_access_error = check_paid_access(user, test_content.video)
        if paid_access_error:
            return paid_access_error

        UserAnswer.objects.filter(test_content=test_content, user=user).delete()

        try:
            stat = UserStatistic.objects.get(video=test_content.video, user=user)
            if stat.true_answer_count > 0:
                stat.true_answer_count -= 1
            elif stat.false_answer_count > 0:
                stat.false_answer_count -= 1
            stat.save()
        except UserStatistic.DoesNotExist:
            pass

        return Response({"message": "Тест сброшен для этого вопроса"})

@extend_schema(
    summary="Создание и получение статистики пользователей",
    description="Этот эндпоинт позволяет создавать и получать статистику пользователей",
    request=UserStatisticSerializer,
    responses={
        200: UserStatisticSerializer,
        201: OpenApiResponse(description="Статистика пользоватлея успешно создана"),
    },
)
@extend_schema(tags=["Video-Statistic: Статистика студентов"])
class UserStatisticViewSet(viewsets.ModelViewSet):
    queryset = UserStatistic.objects.all()
    serializer_class = UserStatisticSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserStatisticFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        for stat in queryset:
            stat.update_accuracy()
        return queryset

@extend_schema(
    summary="Создание и получение ответов пользователей",
    description="Этот эндпоинт позволяет создавать и получать ответы пользоватлеей",
    request=UserAnswerSerializer,
    responses={
        200: UserAnswerSerializer,
        201: OpenApiResponse(description="Ответ пользоватлея успешно создан"),
    },
)
@extend_schema(tags=["Video-Answer: Ответы студентов"])
class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserAnswerFilter
