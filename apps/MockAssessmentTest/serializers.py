from rest_framework import serializers
from .models import Test, TestContent, TestFullDescription, TestInstruction, MockAssessmentTest, MockAssessmentAnswer, UserStatistic
from drf_spectacular.utils import extend_schema_serializer
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse, OpenApiExample, OpenApiParameter


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'test_name', 'last_update_date', 'created_date']

class TestContentSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only=True)
    test_id = serializers.PrimaryKeyRelatedField(
        queryset=Test.objects.all(), source="test", write_only=True
    )

    class Meta:
        model = TestContent
        fields = [
            'id', 'test', 'test_id', 'question_number', 'question_text', 'question_image',
            'additional_questions', 'var_A_image', 'var_B_image', 'var_C_image',
            'var_D_image', 'var_E_image', 'var_A_text', 'var_B_text', 'var_C_text',
            'var_D_text', 'var_E_text', 'true_answer', 'last_update_date', 'created_date'
        ]

class TestFullDescriptionSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only=True)
    test_id = serializers.PrimaryKeyRelatedField(
        queryset=Test.objects.all(), source="test", write_only=True
    )

    class Meta:
        model = TestFullDescription
        fields = ['id', 'test', 'test_id', 'description_title', 'description_image', 'last_update_date', 'created_date']

class TestInstructionSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only=True)
    test_id = serializers.PrimaryKeyRelatedField(
        queryset=Test.objects.all(), source="test", write_only=True
    )

    class Meta:
        model = TestInstruction
        fields = ['id', 'test', 'test_id', 'instruction_title', 'instruction_image', 'last_update_date', 'created_date']

class MockAssessmentTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MockAssessmentTest
        fields = ['id', 'phone_number', 'first_name', 'last_name', 'last_update_date', 'created_date']

class MockAssessmentAnswerSerializer(serializers.ModelSerializer):
    mock_test = MockAssessmentTestSerializer(read_only=True)
    mock_test_id = serializers.PrimaryKeyRelatedField(
        queryset=MockAssessmentTest.objects.all(), source="mock_test", write_only=True
    )
    test_content = TestContentSerializer(read_only=True)
    test_content_id = serializers.PrimaryKeyRelatedField(
        queryset=TestContent.objects.all(), source="test_content", write_only=True
    )

    class Meta:
        model = MockAssessmentAnswer
        fields = [
            'id', 'mock_test', 'mock_test_id', 'test_content', 'test_content_id',
            'question_number', 'answer_vars', 'is_correct', 'last_update_date', 'created_date'
        ]

class UserStatisticSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only=True)
    test_id = serializers.PrimaryKeyRelatedField(
        queryset=Test.objects.all(), source="test", write_only=True
    )
    user = MockAssessmentTestSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=MockAssessmentTest.objects.all(), source="user", write_only=True
    )

    class Meta:
        model = UserStatistic
        fields = [
            'id', 'test', 'test_id', 'user', 'user_id', 'true_answer_count',
            'false_answer_count', 'last_update_date', 'created_date'
        ]

@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Пример запроса',
            value={
                'var': 'А',
                'content': 5,
                'phone_number': '+996555123456',
                'first_name': 'Иван',
                'last_name': 'Петров'
            },
            request_only=True,
            response_only=False,
        )
    ]
)
class MockAssessmentAnswerCreateSerializer(serializers.ModelSerializer):
    var = serializers.CharField(
        help_text="Вариант ответа (А-Д)",
        write_only=True
    )
    content = serializers.PrimaryKeyRelatedField(
        queryset=TestContent.objects.all(),
        write_only=True,
        source='test_content',
        help_text="ID вопроса"
    )
    
    class Meta:
        model = MockAssessmentAnswer
        fields = ['var', 'content']
        extra_kwargs = {
            'test_content': {'read_only': True},
            'answer_vars': {'read_only': True}
        }
