from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import CategoryVideo, Video, TestContent, UserStatistic, UserAnswer
from .serializers import (CategoryVideoSerializer, VideoSerializer, TestContentSerializer, 
                          UserStatisticSerializer, UserAnswerSerializer)
from django.conf import settings

User = get_user_model()

class CategoryVideoViewSet(viewsets.ModelViewSet):
    queryset = CategoryVideo.objects.all()
    serializer_class = CategoryVideoSerializer

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    @action(detail=True, methods=['get'])
    def check_access(self, request, pk=None):
        video = self.get_object()
        user = request.user
        
        if not user.is_authenticated:
            return Response({'error': 'Пользователь не аутентифицирован'}, status=status.HTTP_401_UNAUTHORIZED)

        # Проверка, оплатил ли пользователь контент
        if video.is_paid and not user.paid:
            return Response({'error': 'Доступ запрещен: Контент платный'}, status=status.HTTP_403_FORBIDDEN)

        # Проверка, прошел ли пользователь тест для этого видео
        try:
            statistic = UserStatistic.objects.get(video=video, user=user)
            total_answers = statistic.true_answer_count + statistic.false_answer_count
            if total_answers == 0:  # Пользователь не ответил ни на один вопрос
                return Response({'access': False, 'message': 'Тест не пройден'})
            
            accuracy = statistic.true_answer_count / total_answers
            if accuracy > 0.80:
                return Response({'access': True, 'message': 'Доступ разрешен'})
            else:
                return Response({'access': False, 'message': 'Процент правильных ответов менее 80%'})
        except UserStatistic.DoesNotExist:
            return Response({'access': False, 'message': 'Тест не пройден'})

class TestContentViewSet(viewsets.ModelViewSet):
    queryset = TestContent.objects.all()
    serializer_class = TestContentSerializer

    @action(detail=True, methods=['post'])
    def submit_answer(self, request, pk=None):
        test_content = self.get_object()
        user = request.user

        if not user.is_authenticated:
            return Response({'error': 'Необходимо войти в систему'}, status=status.HTTP_401_UNAUTHORIZED)

        if test_content.video.is_paid and not user.paid:
            return Response({'error': 'Доступ запрещен: Контент платный'}, status=status.HTTP_403_FORBIDDEN)

        answer = request.data.get('answer')
        if answer not in ['a', 'b', 'c', 'd']:
            return Response({'error': 'Неверный формат ответа'}, status=status.HTTP_400_BAD_REQUEST)

        if UserAnswer.objects.filter(test_content=test_content, user=user).exists():
            return Response({'error': 'Вы уже ответили на этот вопрос. Используйте сброс, чтобы пройти снова', 
                            'reset_url': f"{settings.BASE_URL}test-content/{pk}/reset_test/"},
                            status=status.HTTP_403_FORBIDDEN)

        user_answer = UserAnswer.objects.create(test_content=test_content, user=user, answer_vars=answer)
        
        correct = answer == test_content.true_answer
        stat, created = UserStatistic.objects.get_or_create(video=test_content.video, user=user)
        if correct:
            stat.true_answer_count += 1
        else:
            stat.false_answer_count += 1
        stat.save()

        return Response({'message': 'Ответ принят', 'correct': correct})

    @action(detail=True, methods=['post'])
    def reset_test(self, request, pk=None):
        test_content = self.get_object()
        user = request.user

        if not user.is_authenticated:
            return Response({'error': 'Необходимо войти в систему'}, status=status.HTTP_401_UNAUTHORIZED)

        if test_content.video.is_paid and not user.paid:
            return Response({'error': 'Доступ запрещен: Контент платный'}, status=status.HTTP_403_FORBIDDEN)

        # Удаляем только ответ на этот конкретный вопрос
        UserAnswer.objects.filter(test_content=test_content, user=user).delete()

        try:
            stat = UserStatistic.objects.get(video=test_content.video, user=user)
            # Поскольку мы не знаем, был ли ответ правильным, мы просто уменьшаем на 1 любой из счетчиков
            if stat.true_answer_count > 0:
                stat.true_answer_count -= 1
            elif stat.false_answer_count > 0:
                stat.false_answer_count -= 1
            stat.save()
        except UserStatistic.DoesNotExist:
            pass

        return Response({'message': 'Тест сброшен для этого вопроса'})

class UserStatisticViewSet(viewsets.ModelViewSet):
    queryset = UserStatistic.objects.all()
    serializer_class = UserStatisticSerializer

class UserAnswerViewSet(viewsets.ModelViewSet):
    queryset = UserAnswer.objects.all()
    serializer_class = UserAnswerSerializer
