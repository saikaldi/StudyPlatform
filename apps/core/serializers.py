from rest_framework import serializers

from .models import Graduate, AbountTeacher, Feedback

class GraduateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Graduate
        fields = '__all__'
        
        
class AbountTeacherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AbountTeacher
        fields = '__all__'  

class FeedbackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Feedback        
        fields = '__all__'