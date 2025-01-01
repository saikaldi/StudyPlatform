from rest_framework import serializers

from .models import CategoryVideo, Video, Test, UserAnswer, Result


class CategoryVideoSerializer(serializers.ModelSerializer):
    """Сериализатор для модели CategoryVideo"""
    
    class Meta:
        model = CategoryVideo
        fields = "__all__"
        
        
class VideoSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Video"""
    
    class Meta:
        model = Video   
        fields = "__all__"
        

class TestSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Test"""
    
    class Meta:
        model = Test   
        fields = "__all__"
        


class UserAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Answer"""
    
    
    class Meta:
        model = UserAnswer   
        fields = ["student", "answer", "question"]
        
    
class ResultSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Result"""
    
    class Meta:
        model = Result  
        fields = "__all__"


    
