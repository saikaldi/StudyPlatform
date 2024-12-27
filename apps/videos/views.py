from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Course, Video, Purchase,Test
from .serializers import CourseSerializer, VideoSerializer, PurchaseSerializer, TestSerializer

from django.db.models import Q 

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]


def get_queryset(self):
    user = self.request.user
    # Получаем список купленных курсов пользователя
    purchased_courses = Purchase.objects.filter(user=user).values_list('course_id', flat=True)
    # Фильтруем видео, которые либо бесплатные, либо принадлежат к купленным курсам
    return Video.objects.filter(Q(is_free=True) | Q(course__id__in=purchased_courses))

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TestViewSet(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]