from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample, inline_serializer
from rest_framework import serializers
from .models import CategoryVideo, Video, Test, UserAnswer, Result
from .serializers import CategoryVideoSerializer, VideoSerializer, TestSerializer, UserAnswerSerializer, ResultSerializer


@extend_schema(tags=['Category Video Cources'])
class CategoryVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CategoryVideo.objects.all()
    serializer_class = CategoryVideoSerializer

    @extend_schema(
        summary="Получить все категории видео",
        description="Этот эндпоинт возвращает список всех категорий видео",
        responses={
            200: OpenApiResponse(
                description="Список категорий успешно получен",
                response=CategoryVideoSerializer(many=True)
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Получить конкретную категорию видео",
        description="Этот эндпоинт возвращает детали конкретной категории видео по её ID",
        responses={
            200: OpenApiResponse(
                description="Детали категории успешно получены",
                response=CategoryVideoSerializer
            ),
            404: OpenApiResponse(
                description="Категория не найдена",
                examples=[OpenApiExample("Категория не найдена", value={"detail": "Not found"})]
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

@extend_schema(tags=['Video Cources'])
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Video.objects.all()
        else:
            return Video.objects.filter(is_paid=False)

    @extend_schema(
        summary="Получить все видео",
        description="Этот эндпоинт возвращает список всех видео. Для неавторизованных пользователей возвращаются только бесплатные видео",
        responses={
            200: OpenApiResponse(
                description="Список видео успешно получен",
                response=VideoSerializer(many=True)
            )
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Получить конкретное видео",
        description="Этот эндпоинт возвращает детали конкретного видео по его ID. Для платных видео требуется авторизация",
        responses={
            200: OpenApiResponse(
                description="Детали видео успешно получены",
                response=inline_serializer(
                    "VideoDetailResponse",
                    fields={
                        'video': serializers.SerializerMethodField(),
                        'questions': TestSerializer(many=True),
                        'already_passed': serializers.BooleanField(required=False),
                    }
                )
            ),
            403: OpenApiResponse(
                description="Доступ запрещен для неавторизованных пользователей к платному контенту",
                examples=[OpenApiExample("Доступ запрещен", value={"detail": "Доступ запрещен"})]
            ),
            404: OpenApiResponse(
                description="Видео не найдено",
                examples=[OpenApiExample("Видео не найдено", value={"detail": "Not found"})]
            )
        }
    )
    def retrieve(self, request, *args, **kwargs):        
        instance = self.get_object()
        user = request.user
        if instance.is_paid and not user.is_authenticated:
            return Response({"detail": "Доступ запрещен"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance)          
        questions = Test.objects.filter(video=instance)
        questions_serializer = TestSerializer(questions, many=True)
        
        response_data = {
            "video": serializer.data,
            "questions": questions_serializer.data
        }
        if user.is_authenticated and instance.is_already_passed(user):
            response_data["already_passed"] = True
        return Response(response_data)

    @extend_schema(
        summary="Проверка прохождения видео",
        description="Этот эндпоинт проверяет, прошел ли пользователь видео",
        responses={
            200: OpenApiResponse(
                description="Результат проверки на прохождение видео",
                examples=[OpenApiExample("Проверка пройдена", value={"passed": True})]
            ),
            403: OpenApiResponse(
                description="Доступ запрещен для неавторизованных пользователей",
                examples=[OpenApiExample("Доступ запрещен", value={"detail": "Доступ запрещен. Вы не авторизованы"})]
            )
        }
    )
    @action(detail=True, methods=["GET"])
    def check_passed(self, request, pk=None):    
        if not request.user.is_authenticated:
            return Response({"detail": "Доступ запрещен. Вы не авторизованы"}, status=status.HTTP_403_FORBIDDEN)
        video = self.get_object()
        passed = video.is_passed(request.user)
        return Response({"passed": passed})

    @extend_schema(
        summary="Отправить ответ на вопрос",
        description="Этот эндпоинт позволяет пользователю отправить ответ на вопрос из видео",
        request=inline_serializer(
            "SubmitAnswerRequest",
            fields={
                'question_id': serializers.IntegerField(),
                'answer': serializers.CharField(max_length=1),
            }
        ),
        responses={
            201: OpenApiResponse(
                description="Ответ успешно сохранён",
                response=UserAnswerSerializer
            ),
            400: OpenApiResponse(
                description="Ошибка валидации или логики",
                examples=[
                    OpenApiExample("Уже отвечал", value={"detail": "Вы уже ответили на этот вопрос. Изменение ответа запрещено"}),
                    OpenApiExample("Тест пройден", value={"detail": "Вы уже проходили этот тест"}),
                    OpenApiExample("Недостаточно данных", value={"detail": "Отсутствует question_id или answer"})
                ]
            ),
            404: OpenApiResponse(
                description="Вопрос не найден",
                examples=[OpenApiExample("Вопрос не найден", value={"detail": "Вопрос не найден"})]
            )
        }
    )
    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def submit_answer(self, request, pk=None):
        video = self.get_object()
        if video.is_already_passed(request.user):
            return Response({"detail": "Вы уже проходили этот тест"}, status=status.HTTP_400_BAD_REQUEST)

        question_id = request.data.get('question_id')
        answer = request.data.get('answer')

        if not question_id or not answer:
            return Response({"detail": "Отсутствует question_id или answer"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            question = Test.objects.get(id=question_id, video=video)
        except Test.DoesNotExist:
            return Response({"detail": "Вопрос не найден"}, status=status.HTTP_404_NOT_FOUND)

        if UserAnswer.objects.filter(question=question, student=request.user).exists():
            return Response({"detail": "Вы уже ответили на этот вопрос. Изменение ответа запрещено"}, status=status.HTTP_400_BAD_REQUEST)

        user_answer = UserAnswer.objects.create(
            question=question,
            student=request.user,
            answer=answer
        )

        all_questions = Test.objects.filter(video=video)
        answered_questions = UserAnswer.objects.filter(question__video=video, student=request.user)

        if all_questions.count() == answered_questions.count():
            correct_answers = sum(1 for answer in answered_questions if answer.is_correct())
            total_questions = all_questions.count()
            result_percentage = (correct_answers / total_questions) * 100
            passed = result_percentage >= 80

            result, created = Result.objects.update_or_create(
                student=request.user,
                video=video,
                defaults={
                    'total_questions': total_questions,
                    'correct_answers': correct_answers,
                    'incorrect_answers': total_questions - correct_answers,
                    'result_percentage': result_percentage,
                    'passed': passed
                }
            )

        serializer = UserAnswerSerializer(user_answer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Сбросить тест",
        description="Этот эндпоинт сбрасывает все ответы и результаты для указанного видео, позволяя пользователю пройти тест снова",
        responses={
            200: OpenApiResponse(
                description="Тест успешно сброшен",
                examples=[OpenApiExample("Тест сброшен", value={"detail": "Тест сброшен, вы можете пройти его снова"})]
            ),
            400: OpenApiResponse(
                description="Тест не был пройден",
                examples=[OpenApiExample("Тест не пройден", value={"detail": "Вы еще не проходили этот тест"})]
            )
        }
    )
    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def reset_test(self, request, pk=None):
        video = self.get_object()
        if not video.is_already_passed(request.user):
            return Response({"detail": "Вы еще не проходили этот тест"}, status=status.HTTP_400_BAD_REQUEST)

        UserAnswer.objects.filter(question__video=video, student=request.user).delete()
        Result.objects.filter(student=request.user, video=video).delete()
        return Response({"detail": "Тест сброшен, вы можете пройти его снова"}, status=status.HTTP_200_OK)

@extend_schema(tags=['Video Test'])
class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer  

    @extend_schema(
        summary="Получить тесты по видео",
        description="Этот эндпоинт возвращает тесты для конкретного видео",
        responses={
            200: OpenApiResponse(
                description="Тесты успешно получены",
                response=TestSerializer(many=True)
            ),
            404: OpenApiResponse(
                description="Тесты для видео не найдены",
                examples=[OpenApiExample("Тесты не найдены", value={"detail": "Тесты для данного видео не найдены"})]
            )
        }
    )
    @action(detail=False, methods=['GET'], url_path='by-video/(?P<video_id>[^/.]+)', permission_classes=[IsAuthenticated])
    def get_tests_by_video(self, request, video_id=None):
        tests = Test.objects.filter(video_id=video_id)
        if not tests.exists():
            return Response({"detail": "Тесты для данного видео не найдены"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(tests, many=True)
        return Response(serializer.data)

@extend_schema(tags=['User Answer for Video Test'])
class AnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()    
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserAnswer.objects.filter(student=self.request.user)

@extend_schema(tags=['User Test Video Result'])
class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()    
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Result.objects.filter(student=self.request.user)

    @extend_schema(
        summary="Сбросить ответы для видео",
        description="Этот эндпоинт сбрасывает все ответы и результаты для указанного видео",
        responses={
            200: OpenApiResponse(
                description="Ответы и результаты успешно сброшены",
                examples=[OpenApiExample("Сброс выполнен", value={"detail": "Все ответы и результаты сброшены для указанного видео"})]
            )
        }
    )
    @action(detail=False, methods=['POST'], url_path='reset-answers/(?P<video_id>[^/.]+)', permission_classes=[IsAuthenticated])
    def reset_answers(self, request, video_id=None):
        UserAnswer.objects.filter(question__video_id=video_id, student=request.user).delete()
        Result.objects.filter(video_id=video_id, student=request.user).delete()
        return Response({"detail": "Все ответы и результаты сброшены для указанного видео"}, status=status.HTTP_200_OK)
