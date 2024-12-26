from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import Graduate, AbountTeacher, Feedback
from .serializers import GraduateSerializer, AbountTeacherSerializer, FeedbackSerializer

# Create your views here.



class GraduateView(viewsets.ModelViewSet):
    queryset = Graduate.objects.all()   
    serializer_class = GraduateSerializer
    
        
class AbountTeacherView(viewsets.ModelViewSet):
    queryset = AbountTeacher.objects.all()
    serializer_class = AbountTeacherSerializer

    
class FeedbackView(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()   
    serializer_class = FeedbackSerializer   
    

    