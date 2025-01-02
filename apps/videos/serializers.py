from rest_framework import serializers

from .models import CategoryVideo, Video, Test, UserAnswer, Result


class CategoryVideoSerializer(serializers.ModelSerializer):
    """Сериализатор для модели CategoryVideo"""
    
    class Meta:
        model = CategoryVideo
        fields = ['id', 'name']
        
class VideoSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Video"""
    
    class Meta:
        model = Video   
        fields = ['id', 'subject', 'description', 'category', 'video_url', 'is_paid']
        

class TestSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Test"""
    
    class Meta:
        model = Test   
        fields = "__all__"
        


class UserAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Answer"""
    
    
    class Meta:
        model = UserAnswer   
        fields = ["id", "student", "answer", "question"]
        
    
class ResultSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Result"""
    
    class Meta:
        model = Result  
        fields = "__all__"


    
