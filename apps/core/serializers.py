from rest_framework import serializers

from .models import Graduate, AbountTeacher, Feedback, TeacherType

class TeacherTypeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TeacherType        
        fields = ['id', 'name', 'parent', 'created_data']

class GraduateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Graduate
        fields = ['id', 'name', 'lastname', 'image', 'score', 'review', 'created_data']
        
        
class AbountTeacherSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AbountTeacher
        fields = ['id', 'name', 'lastname', 'image', 'teacher_type', 'created_data']

class FeedbackSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Feedback        
        fields = ['id', 'name', 'lastname', 'gmail', 'phone_number', 'text', 'created_data']