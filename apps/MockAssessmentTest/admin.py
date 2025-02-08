from django.contrib import admin
from .models import MockAssessmentTest, MockAssessmentTestContent, MockAssessmentTestFullDescription, MockAssessmentTestInstruction, MockAssessmentUser, MockAssessmentAnswer, MockAssessmentUserStatistic


class MockAssessmentTestContentInline(admin.TabularInline):
    model = MockAssessmentTestContent
    extra = 0  # не показывать дополнительные пустые формы

class MockAssessmentTestFullDescriptionInline(admin.TabularInline):
    model = MockAssessmentTestFullDescription
    extra = 0

class MockAssessmentTestInstructionInline(admin.TabularInline):
    model = MockAssessmentTestInstruction
    extra = 0

# class MockAssessmentUserStatisticInline(admin.TabularInline):
#     model = MockAssessmentUserStatistic
#     extra = 0

@admin.register(MockAssessmentTest)
class MockAssessmentTestAdmin(admin.ModelAdmin):
    list_display = ('test_name', 'last_update_date', 'created_date')
    inlines = [MockAssessmentTestContentInline, MockAssessmentTestFullDescriptionInline, MockAssessmentTestInstructionInline]

@admin.register(MockAssessmentTestContent)
class MockAssessmentTestContentAdmin(admin.ModelAdmin):
    list_display = ('test', 'question_number', 'question_text', 'true_answer', 'last_update_date')
    list_filter = ('test',)
    search_fields = ['question_text']

@admin.register(MockAssessmentTestFullDescription)
class MockAssessmentTestFullDescriptionAdmin(admin.ModelAdmin):
    list_display = ('test', 'description_title', 'last_update_date', 'created_date')
    list_filter = ('test',)

@admin.register(MockAssessmentTestInstruction)
class MockAssessmentTestInstructionAdmin(admin.ModelAdmin):
    list_display = ('test', 'instruction_title', 'last_update_date', 'created_date')
    list_filter = ('test',)

@admin.register(MockAssessmentAnswer)
class MockAssessmentAnswerAdmin(admin.ModelAdmin):
    list_display = ('mock_test', 'test_content', 'question_number', 'answer_vars', 'is_correct', 'last_update_date')
    list_filter = ('mock_test', 'is_correct')
    search_fields = ['mock_test__first_name', 'mock_test__last_name']

from django.contrib import admin
from .models import MockAssessmentTest, MockAssessmentTestContent, MockAssessmentTestFullDescription, MockAssessmentTestInstruction, MockAssessmentUser, MockAssessmentAnswer, MockAssessmentUserStatistic

class MockAssessmentUserStatisticInline(admin.TabularInline):
    model = MockAssessmentUserStatistic  # This inline should be for statistics, not directly linked to itself
    extra = 0  # не показывать дополнительные пустые формы

@admin.register(MockAssessmentUser)
class MockAssessmentUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'last_update_date', 'created_date')
    search_fields = ['first_name', 'last_name', 'phone_number']
    inlines = [MockAssessmentUserStatisticInline]  # Place the inline here to show statistics for each user

@admin.register(MockAssessmentUserStatistic)
class MockAssessmentUserStatisticAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'true_answer_count', 'false_answer_count', 'last_update_date')
    list_filter = ('test',)
    search_fields = ['user__first_name', 'user__last_name']
    # Remove the inlines here since it's not appropriate for this model to have an inline of itself

# Other admin configurations remain unchanged