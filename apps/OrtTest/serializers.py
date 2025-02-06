from rest_framework import serializers
from .models import (
    TestCategory,
    Test,
    TestContent,
    TestFullDescription,
    UserAnswer,
    UserStatistic,
    SubjectCategory,
    OkupTushunuuText,
    TestInstruction,
    UserStatistic,
    UserAnswer,
    OkupTushunuu,
    OkupTushunuuQuestion,
)


class TestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCategory
        fields = ["id", "test_category_name", "last_update_date", "created_date"]


class SubjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectCategory
        fields = "__all__"


class TestContentSerializer(serializers.ModelSerializer):
    # test = TestSerializer(read_only=True)
    test_id = serializers.PrimaryKeyRelatedField(
        queryset=Test.objects.all(), source="test", write_only=True
    )

    class Meta:
        model = TestContent
        fields = [
            "id",
            "test",
            "test_id",
            "question_text",
            "question_image",
            "var_A_image",
            "var_B_image",
            "var_C_image",
            "var_D_image",
            "var_E_image",
            "var_A_text",
            "var_B_text",
            "var_C_text",
            "var_D_text",
            "var_E_text",
            "additional_questions",
            "true_answer",
            "question_number",
            "last_update_date",
            "created_date",
        ]


class TestSerializer(serializers.ModelSerializer):
    test_category = TestCategorySerializer(read_only=True)
    test_category_id = serializers.PrimaryKeyRelatedField(queryset=TestCategory.objects.all(), source="test_category", write_only=True)
    subject_category = SubjectCategorySerializer(read_only=True)
    subject_category_id = serializers.PrimaryKeyRelatedField(queryset=SubjectCategory.objects.all(), source="subject_category", write_only=True)
    test_questions = serializers.SerializerMethodField()

    class Meta:
        model = Test
        fields = [
            "id",
            "test_category",
            "test_category_id",
            "subject_category",
            "subject_category_id",
            "title",
            "first_test",
            "description",
            "background_image",
            "test_questions",
            "last_update_date",
            "created_date",
        ]

    def get_test_questions(self, obj):
        test_questions = TestContent.objects.filter(test=obj)
        return TestContentSerializer(test_questions, many=True).data


class TestFullDescriptionSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only=True)
    test_id = serializers.PrimaryKeyRelatedField(
        queryset=Test.objects.all(), source="test", write_only=True
    )

    class Meta:
        model = TestFullDescription
        fields = [
            "id",
            "test",
            "test_id",
            "description_title",
            "description_image",
            "last_update_date",
            "created_date",
        ]


class TestInstructionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestInstruction
        fields = [
            "id",
            "instruction_title",
            "instruction_image",
            "last_update_date",
            "created_date",
        ]


class UserAnswerSerializer(serializers.ModelSerializer):
    test_content = TestContentSerializer(read_only=True)
    test_content_id = serializers.PrimaryKeyRelatedField(
        queryset=TestContent.objects.all(), source="test_content", write_only=True
    )

    class Meta:
        model = UserAnswer
        fields = [
            "id",
            "user",
            "okup_tushunuu_question",
            "test_content",
            "test_content_id",  # Обязательно указываем
            "answer_vars",
            "last_update_date",
            "created_date",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)


class UserStatisticSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only=True)
    test_id = serializers.PrimaryKeyRelatedField(
        queryset=Test.objects.all(), source="test", write_only=True
    )

    class Meta:
        model = UserStatistic
        fields = [
            "id",
            "user",
            "test",
            "okup_tushunuu",
            "true_answer_count",
            "false_answer_count",
            "last_update_date",
            "created_date",
        ]


class OkupTushunuuSerializer(serializers.ModelSerializer):
    class Meta:
        model = OkupTushunuu
        fields = ["id", "name", "description", "created_at"]


class OkupTushunuuTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = OkupTushunuuText
        fields = "__all__"


class OkupTushunuuQuestionSerializer(serializers.ModelSerializer):
    okup_tushunuu = OkupTushunuuSerializer(read_only=True)
    okup_tushunuu_id = serializers.PrimaryKeyRelatedField(
        queryset=OkupTushunuu.objects.all(), source="okup_tushunuu", write_only=True
    )

    # okup_tushunuu_text = OkupTushunuuTextSerializer(read_only=True)
    # okup_tushunuu_text_id = serializers.PrimaryKeyRelatedField(queryset=OkupTushunuuText.objects.all(), source="okup_tushunuu_text", write_only=True)
    class Meta:
        model = OkupTushunuuQuestion
        fields = [
            "id",
            "okup_tushunuu",
            "okup_tushunuu_id",
            # "okup_tushunuu_text",
            # "okup_tushunuu_text_id",
            "question",
            "question_number",
            "question_text",
            "var_A_text",
            "var_B_text",
            "var_C_text",
            "var_D_text",
            "var_E_text",
            "true_answer",
        ]
