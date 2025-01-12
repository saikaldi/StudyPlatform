from rest_framework import serializers
from .models import TestCategory, Test, TestContent, TestFullDescription, TestInstruction, AdditionalInstruction, UserAnswer, UserStatistic


class TestCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCategory
        fields = ['id', 'test_category_name']

class TestSerializer(serializers.ModelSerializer):
    test_category = TestCategorySerializer(read_only=True)
    test_category_id = serializers.PrimaryKeyRelatedField(queryset=TestCategory.objects.all(), source='test_category', write_only=True)

    class Meta:
        model = Test
        fields = ['id', 'test_category', 'test_category_id', 'title', 'first_test', 'description', 'background_image']

class TestContentSerializer(serializers.ModelSerializer):
    test = TestSerializer(read_only=True)
    test_id = serializers.PrimaryKeyRelatedField(queryset=Test.objects.all(), source='test', write_only=True)

    class Meta:
        model = TestContent
        fields = ['id', 'test', 'test_id', 'question', 'var_A_image', 'var_B_image', 'var_C_image', 'var_D_image', 
                  'var_A_text', 'var_B_text', 'var_C_text', 'var_D_text', 'true_answer', 'timer']

class TestFullDescriptionSerializer(serializers.ModelSerializer):
    test_category = TestCategorySerializer(read_only=True)
    test_category_id = serializers.PrimaryKeyRelatedField(queryset=TestCategory.objects.all(), source='test_category', write_only=True)

    class Meta:
        model = TestFullDescription
        fields = ['id', 'test_category', 'test_category_id', 'description_title', 'description']

class TestInstructionSerializer(serializers.ModelSerializer):
    test_category = TestCategorySerializer(read_only=True)
    test_category_id = serializers.PrimaryKeyRelatedField(queryset=TestCategory.objects.all(), source='test_category', write_only=True)

    class Meta:
        model = TestInstruction
        fields = ['id', 'test_category', 'test_category_id', 'instruction_title', 'instruction']

class AdditionalInstructionSerializer(serializers.ModelSerializer):
    testing_instruction = TestInstructionSerializer(read_only=True)
    testing_instruction_id = serializers.PrimaryKeyRelatedField(queryset=TestInstruction.objects.all(), source='testing_instruction', write_only=True)

    class Meta:
        model = AdditionalInstruction
        fields = ['id', 'testing_instruction', 'testing_instruction_id', 'additional_title', 'additional_description']

class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAnswer
        fields = ['test_content', 'answer_vars']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

class UserStatisticSerializer(serializers.ModelSerializer):
    test = TestContentSerializer(read_only=True)
    test_id = serializers.PrimaryKeyRelatedField(queryset=TestContent.objects.all(), source='test', write_only=True)

    class Meta:
        model = UserStatistic
        fields = ['id', 'test', 'test_id', 'user', 'true_answer_count', 'false_answer_count']
