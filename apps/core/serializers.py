from rest_framework import serializers

from .models import Graduate, AbountUs, Feedback

class GraduateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Graduate
        fields = '__all__'
        
        
class AbountUsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AbountUs
        fields = '__all__'  

class FeedbackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Feedback        
        fields = '__all__'