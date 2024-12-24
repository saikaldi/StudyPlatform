from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from .models import Graduate, AbountUs, Feedback
from .serializers import GraduateSerializer, AbountUsSerializer, FeedbackSerializer

# Create your views here.



class GraduateView(viewsets.ModelViewSet):
    queryset = Graduate.objects.all()   
    serializer_class = GraduateSerializer
    
        
class AbountUsView(viewsets.ModelViewSet):
    queryset = AbountUs.objects.all()
    serializer_class = AbountUsSerializer
    
    
class FeedbackView(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()   
    serializer_class = FeedbackSerializer   
    

    