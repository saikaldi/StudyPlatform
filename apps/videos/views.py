from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status, permissions


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
        """
        
        """
        1                                
        instance = self.get_object()
        if instance.is_paid and not request.user.is_authenticated:
            return Response({"detail": "Доступ запрещен"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    
class TestViewSet(viewsets.ModelViewSet):
    """Модель для сохранения информации о вопросах урока"""
    
    queryset = Test.objects.all()
    serializer_class = TestSerializer  
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    
class AnswerViewSet(viewsets.ModelViewSet):
    """Модель для сохранения информации о ответах на вопросы урока"""
  
    queryset = UserAnswer.objects.all()    
    serializer_class = UserAnswerSerializer
    
    
    def list(self, request):
        """Метод для получения списка ответов на вопросы урока"""
        
        queryset = Test.objects.all()
        serializer = TestSerializer(queryset, many=True)
        return Response(serializer.data)
     


class ResultViewSet(viewsets.ModelViewSet):
    """Модель для сохранения информации о результатах теста"""
    
    queryset = Result.objects.all()    
    serializer_class = ResultSerializer
    
    