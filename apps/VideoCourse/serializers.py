from rest_framework import serializers
from .models import (
    CategoryVideo,
    Video,
    TestContent,
    UserStatistic,
    UserAnswer,
    SubjectCategory,
    Category,
)
from .serializers import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "category_name", "last_update_date", "created_date"]
        read_only_fields = ["slug", "last_update_date", "created_date"]


class CategoryVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryVideo
        fields = ["id", "category_name", "last_update_date", "created_date"]
        read_only_fields = ["slug", "last_update_date", "created_date"]


class SubjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectCategory
        fields = "__all__"
        read_only_fields = ["last_update_date", "created_date"]


class VideoSerializer(serializers.ModelSerializer):
    subject_category = SubjectCategorySerializer(read_only=True)
    subject_category_id = serializers.PrimaryKeyRelatedField(queryset=SubjectCategory.objects.all(), source="subject_category", write_only=True)

    video_category = CategoryVideoSerializer(read_only=True)
    video_category_id = serializers.PrimaryKeyRelatedField(queryset=CategoryVideo.objects.all(), source="video_category", write_only=True)

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source="category", write_only=True)

    class Meta:
        model = Video
        fields = [
            "id",
            "category",
            "category_id",
            "video_category",
            "video_category_id",
            "subject_name",
            "subject_category",
            "subject_category_id",
            "description",
            "video_url",
            "video_order",
            "is_paid",
            "last_update_date",
            "created_date",
        ]
        read_only_fields = ["slug", "last_update_date", "created_date"]


class TestContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestContent
        fields = "__all__"
        read_only_fields = ["last_update_date", "created_date", "slug"]


class UserStatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserStatistic
        fields = [
            "id",
            "user",
            "video",
            "true_answer_count",
            "false_answer_count",
            "accuracy_percentage",
            "last_update_date",
            "created_date",
        ]
        read_only_fields = ["last_update_date", "created_date", "accuracy_percentage"]


class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = [
            "id",
            "test_content",
            "user",
            "answer_vars",
            "output_time",
            "last_update_date",
            "created_date",
        ]
        read_only_fields = ["last_update_date", "created_date"]
