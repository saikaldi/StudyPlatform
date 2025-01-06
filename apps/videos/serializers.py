from rest_framework import serializers

from .models import CategoryVideo, Video, Test, UserAnswer, Result


class CategoryVideoSerializer(serializers.ModelSerializer):
    """Сериализатор для модели CategoryVideo"""
    parent = serializers.SerializerMethodField()
    
    class Meta:
        model = CategoryVideo
        fields = ['id', 'name', 'parent']
        
    def get_parent(self, obj):
        if obj.parent:
            return CategoryVideoSerializer(obj.parent).data
        return None
        
        
class VideoSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Video"""
    category = CategoryVideoSerializer(read_only=True)
    
    
    class Meta:
        model = Video   
        fields = [ 'id', 'category',  'subject', 'description',  'video_url', 'is_paid']
        

class TestSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Test"""
    
    class Meta:
        model = Test   
        fields = "__all__"
        
        
class VideoSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Video"""
    category = CategoryVideoSerializer(read_only=True)    
    
    class Meta:
        model = Video   
        fields = [ 'id', 'category',  'subject', 'description',  'video_url', 'is_paid']
        

        


class UserAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Answer"""
    
    class Meta:
        model = UserAnswer   
        fields = ["id", "student", "answer", "question"]
        
    
class ResultSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Result"""
    
    class Meta:
        model = Result  
        fields = ["id", "student", "video", "total_questions", "correct_answers", "incorrect_answers", "result_percentage", "created_data"]


    
