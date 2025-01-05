from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404


from .models import CategoryVideo, Video, Test, UserAnswer, Result
from .serializers import CategoryVideoSerializer, VideoSerializer,  TestSerializer, UserAnswerSerializer, ResultSerializer


class CategoryVideoViewSet(viewsets.ReadOnlyModelViewSet):
    """Модель для сохранения информации о категориях видео"""
    
    queryset = CategoryVideo.objects.all()
    serializer_class = CategoryVideoSerializer

    
class VideoViewSet(viewsets.ModelViewSet):
    """Модель для сохранения информации о видео"""
    
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
   
    
    def get_queryset(self):
        """
        Метод для получения списка видео по категории платный или бесплатный
        """
        user = self.request.user
        if user.is_authenticated:
            return Video.objects.all()
        else:
            return Video.objects.filter(is_paid=False)
    @action(detail=True, methods=["GET"])
    def check_passed(self, request, pk=None):
        video = self.get_object()
        passed = video.is_passed(request.user)
        return Response({"passed": passed})
    
         
    def retrieve(self, request, *args, **kwargs):        
        """ Метод для получения информации о видео """
                             
        instanse = self.get_object()
        user = request.user
        if instanse.is_paid and not user.has_paid_for_video(instanse):              # проверка на платность видео
            return Response({"detail": "Доступ запрещен"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instanse)
        return Response(serializer.data)
    
    
    def submit_answers(self, request, video_id):
        """Метод для отправки ответа на вопрос урока"""
        if not request.user.is_authenticated:
            return Response({"detail": "Доступ запрещен. Вы не авторизованы"}, status=status.HTTP_403_FORBIDDEN)
        
        student = request.user
        
        video = get_object_or_404(Video, id=video_id)
        answers = request.data.get('answers', [])  # получаем ответы пользователя
        correct_count = 0  # счетчик правильных ответов
        incorrect_count = 0  # счетчик неправильных ответов
        
        for answer_data in answers:
            question_id = answer_data.get('question_id')
            answer = answer_data.get('answer')

            try:
                question = Test.objects.get(id=question_id, video=video)
            except Test.DoesNotExist:
                return Response({"detail": f"{question_id} < не правилный ID "}, status=status.HTTP_400_BAD_REQUEST)

            user_answer = UserAnswer(
                question=question,
                student=request.user,
                answer=answer
            )
            user_answer.save()

            if user_answer.is_correct():
                correct_count += 1                   # увеличиваем счетчик правильных ответов
                answer_data['correct'] = True
            else:
                incorrect_count += 1
                answer_data['correct'] = False
                    
        total_questions = video.get_total_questions()
        if correct_count == 0:
            return Response({'message': 'Вы не прошли урок.Смотрите видео урок и сдайте тест ище раз ', 
                             'total_questions': total_questions,
                            'correct_count': correct_count},
                            status=status.HTTP_400_BAD_REQUEST)
            
        result = (correct_count / total_questions) * 100
        
        result_obj = Result(
            student=request.user,
            video=video,
            total_questions=total_questions,
            correct_answers=correct_count,
            incorrect_answers=incorrect_count,
            result_percentage=result
        )
        result_obj.save()      
          
        if result >= 80:
            return Response({ 
                            'message': 'Поздравляем вы прошли урок.',
                            'total_questions': total_questions,
                            'result': result,
                            'correct_count': correct_count,
                            'incorrect_count': incorrect_count,
                            'questions': answers},
                            status=status.HTTP_200_OK)
        
        return Response({
            'message': 'Вы не прошли урок. Повторно сдайте тест',
            'total_questions': total_questions,
            'result': result,
            'correct_count': correct_count,
            'incorrect_count': incorrect_count,
            'questions': answers},
            status=status.HTTP_400_BAD_REQUEST)
    
class TestViewSet(viewsets.ModelViewSet):
    """Модель для сохранения информации о вопросах урока"""
    
    queryset = Test.objects.all()
    serializer_class = TestSerializer  

    
    def get_queryset(self):
        """
        Метод для получения списка вопросов по видео 
         платный или бесплатный
        """
        user = self.request.user
        if user.is_authenticated:
            return Test.objects.all()
        else:
            return Test.objects.filter(is_paid=False)
        
        
    def retrieve(self, request, *args, **kwargs):
        """Метод для получения информации о вопросе"""
        instance = self.get_object()
        if instance.is_paid and not request.user.is_authenticated:
            return Response({"detail": "Доступ запрещен"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    

    
class AnswerViewSet(viewsets.ModelViewSet):
    """Модель для сохранения информации о ответах на вопросы урока"""
    
   
    queryset = UserAnswer.objects.all()    
    serializer_class = UserAnswerSerializer
    
    
    def get_queryset(self):
    
        user = self.request.user
        if user.is_authenticated:
            return UserAnswer.objects.filter(student=user)
        else:
            return UserAnswer.objects.filter(student__is_status_approved=False)




    
    

class ResultViewSet(viewsets.ModelViewSet):
    """Модель для сохранения информации о результатах теста"""
    
    queryset = Result.objects.all()    
    serializer_class = ResultSerializer
    
    
    
    


    
