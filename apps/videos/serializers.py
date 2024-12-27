from rest_framework import serializers
from .models import Course, Video, Test, Purchase

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class VideoSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    
    class Meta:
        model = Video
        fields = ['id', 'course', 'title', 'url', 'is_free']

class TestSerializer(serializers.ModelSerializer):
    video = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Test
        fields = ['id', 'video', 'question', 'answer']

class PurchaseSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Purchase
        fields = ['id', 'user', 'course', 'purchase_date']