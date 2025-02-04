from django.contrib import admin
from .models import Test, TestContent, TestFullDescription, TestInstruction, MockAssessmentTest, MockAssessmentAnswer, UserStatistic

class TestContentInline(admin.TabularInline):
    model = TestContent
    extra = 0  # не показывать дополнительные пустые формы

class TestFullDescriptionInline(admin.TabularInline):
    model = TestFullDescription
    extra = 0

class TestInstructionInline(admin.TabularInline):
    model = TestInstruction
    extra = 0

class UserStatisticInline(admin.TabularInline):
    model = UserStatistic
    extra = 0

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'last_update_date', 'created_date')
    inlines = [TestContentInline, TestFullDescriptionInline, TestInstructionInline]

@admin.register(TestContent)
class TestContentAdmin(admin.ModelAdmin):
    list_display = ('test', 'question_number', 'question_text', 'true_answer', 'last_update_date')
    list_filter = ('test',)
    search_fields = ['question_text']

@admin.register(TestFullDescription)
class TestFullDescriptionAdmin(admin.ModelAdmin):
    list_display = ('test', 'description_title', 'last_update_date', 'created_date')
    list_filter = ('test',)

@admin.register(TestInstruction)
class TestInstructionAdmin(admin.ModelAdmin):
    list_display = ('test', 'instruction_title', 'last_update_date', 'created_date')
    list_filter = ('test',)

@admin.register(MockAssessmentTest)
class MockAssessmentTestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'last_update_date', 'created_date')
    search_fields = ['first_name', 'last_name', 'phone_number']
    inlines = [UserStatisticInline]

@admin.register(MockAssessmentAnswer)
class MockAssessmentAnswerAdmin(admin.ModelAdmin):
    list_display = ('mock_test', 'test_content', 'question_number', 'answer_vars', 'is_correct', 'last_update_date')
    list_filter = ('mock_test', 'is_correct')
    search_fields = ['mock_test__first_name', 'mock_test__last_name']

@admin.register(UserStatistic)
class UserStatisticAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'true_answer_count', 'false_answer_count', 'last_update_date')
    list_filter = ('test',)
    search_fields = ['user__first_name', 'user__last_name']
