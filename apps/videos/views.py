from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from .models import CategoryVideo, Video, Test, UserAnswer, Result
from .serializers import CategoryVideoSerializer, VideoSerializer,  TestSerializer, UserAnswerSerializer, ResultSerializer


class CategoryVideoViewSet(viewsets.ModelViewSet):
    """Модель для сохранения информации о категориях видео"""
    
    queryset = CategoryVideo.objects.all()
    serializer_class = CategoryVideoSerializer
    
    
    
class VideoViewSet(viewsets.ModelViewSet):
    """Модель для сохранения информации о видео"""
    
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    
    def get_queryset(self):
        """
        Метод для получения списка видео по категории 
         платный или бесплатный
        """
        
        user = self.request.user
        if user.is_authenticated:
            return Video.objects.all()
        else:
            return Video.objects.filter(is_paid=False)
        
        
    def retrieve(self, request, *args, **kwargs):        
        """ Метод для получения информации о видео """
                             
        instance = self.get_object()
        if instance.is_paid and not request.user.is_authenticated:
            return Response({"detail": "Доступ запрещен"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    
    
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
        
    def retrieve(self, request, *args, **kwargs):
        """Метод для получения информации о ответе"""
        instance = self.get_object()
        if request.user.is_authenticated:            
            return Response({"detail": "Доступ запрещен"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserAnswersView(APIView):
    permission_classes = [IsAuthenticated] 
    """ Метод для получения информации о ответах на вопросы урока"""

    def get(self, request):
        user = request.user
        user_answers = UserAnswer.objects.filter(student=user)
        
    
        answers = []
        for answer in user_answers:
            answers.append({       
                'id_test': answer.question.id_question,
                'question': answer.question.text,
                'user_answer': answer.answer,
                'correct_answer': answer.question.is_correct,
                'is_correct': answer.is_correct(),
            })
        
        return Response(answers, status=status.HTTP_200_OK)
    
    

class ResultViewSet(viewsets.ModelViewSet):
    """Модель для сохранения информации о результатах теста"""
    
    queryset = Result.objects.all()    
    serializer_class = ResultSerializer
    