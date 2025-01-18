from rest_framework import serializers
from .models import CategoryVideo, Video, TestContent, UserStatistic, UserAnswer

class CategoryVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryVideo
        fields = ['category_name', 'last_update_date', 'created_date']
        read_only_fields = ['slug', 'last_update_date', 'created_date']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['video_category', 'subject_name', 'description', 'video_url', 'video_order', 'is_paid', 'last_update_date', 'created_date']
        read_only_fields = ['slug', 'last_update_date', 'created_date']

class TestContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestContent
        fields = '__all__'
        read_only_fields = ['last_update_date', 'created_date', 'slug']

class UserStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatistic
        fields = ['user', 'video', 'true_answer_count', 'false_answer_count', 'accuracy_percentage', 'last_update_date', 'created_date']
        read_only_fields = ['last_update_date', 'created_date', 'accuracy_percentage']

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['test_content', 'user', 'answer_vars', 'output_time', 'last_update_date', 'created_date']
        read_only_fields = ['last_update_date', 'created_date']
