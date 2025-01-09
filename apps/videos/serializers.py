from rest_framework import serializers
from .models import CategoryVideo, Video, Test, UserAnswer, Result


class CategoryVideoSerializer(serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    
    class Meta:
        model = CategoryVideo
        fields = ['id', 'name', 'parent']
        
    def get_parent(self, obj):
        if obj.parent:
            return CategoryVideoSerializer(obj.parent).data
        return None

class VideoSerializer(serializers.ModelSerializer):
    category = CategoryVideoSerializer(read_only=True)

    class Meta:
        model = Video   
        fields = ['id', 'category', 'subject', 'description', 'video_url', 'is_paid']

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test   
        fields = "__all__"

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer   
        fields = ["id", "student", "answer", "question"]
        read_only_fields = ['student']

    def create(self, validated_data):
        question = validated_data['question']
        student = self.context['request'].user
        if UserAnswer.objects.filter(question=question, student=student).exists():
            raise serializers.ValidationError("Вы уже ответили на этот вопрос")
        return super().create(validated_data)

class ResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Result  
        fields = ["id", "student", "video", "total_questions", "correct_answers", "incorrect_answers", "result_percentage", "created_data", "passed"]
