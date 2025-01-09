from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import CategoryVideo, Video, Test, UserAnswer, Result
from .serializers import CategoryVideoSerializer, VideoSerializer, TestSerializer, UserAnswerSerializer, ResultSerializer


class CategoryVideoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CategoryVideo.objects.all()
    serializer_class = CategoryVideoSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Video.objects.all()
        else:
            return Video.objects.filter(is_paid=False)

    @action(detail=True, methods=["GET"])
    def check_passed(self, request, pk=None):    
        if not request.user.is_authenticated:
            return Response({"detail": "Доступ запрещен. Вы не авторизованы"}, status=status.HTTP_403_FORBIDDEN)
        video = self.get_object()
        passed = video.is_passed(request.user)
        return Response({"passed": passed})

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

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def reset_test(self, request, pk=None):
        video = self.get_object()
        if not video.is_already_passed(request.user):
            return Response({"detail": "Вы еще не проходили этот тест"}, status=status.HTTP_400_BAD_REQUEST)

        UserAnswer.objects.filter(question__video=video, student=request.user).delete()
        Result.objects.filter(student=request.user, video=video).delete()
        return Response({"detail": "Тест сброшен, вы можете пройти его снова"}, status=status.HTTP_200_OK)

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer  

    @action(detail=False, methods=['GET'], url_path='by-video/(?P<video_id>[^/.]+)', permission_classes=[IsAuthenticated])
    def get_tests_by_video(self, request, video_id=None):
        tests = Test.objects.filter(video_id=video_id)
        if not tests.exists():
            return Response({"detail": "Тесты для данного видео не найдены"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(tests, many=True)
        return Response(serializer.data)

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()    
    serializer_class = UserAnswerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserAnswer.objects.filter(student=self.request.user)

class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()    
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Result.objects.filter(student=self.request.user)

    @action(detail=False, methods=['POST'], url_path='reset-answers/(?P<video_id>[^/.]+)', permission_classes=[IsAuthenticated])
    def reset_answers(self, request, video_id=None):
        UserAnswer.objects.filter(question__video_id=video_id, student=request.user).delete()
        Result.objects.filter(video_id=video_id, student=request.user).delete()
        return Response({"detail": "Все ответы и результаты сброшены для указанного видео"}, status=status.HTTP_200_OK)
