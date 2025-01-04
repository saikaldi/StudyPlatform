from django.contrib import admin
from .models import (
    TestCategory, 
    Test, 
    TestContent, 
    TestFullDescription, 
    TestInstruction, 
    AdditionalInstruction, 
    UserAnswer, 
    UserStatistic
)

@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'test_category_name', 'last_update_date', 'created_date')
    search_fields = ('test_category_name',)
    list_filter = ('created_date', 'last_update_date')

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'test_category', 'first_test', 'last_update_date', 'created_date')
    search_fields = ('title', 'description')
    list_filter = ('test_category', 'first_test', 'last_update_date', 'created_date')

@admin.register(TestContent)
class TestContentAdmin(admin.ModelAdmin):
    list_display = ('id', 'test', 'question', 'true_answer', 'timer', 'last_update_date', 'created_date')
    search_fields = ('question', 'true_answer')
    list_filter = ('test', 'last_update_date', 'created_date')

@admin.register(TestFullDescription)
class TestFullDescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'test_category', 'description_title', 'last_update_date', 'created_date')
    search_fields = ('description_title', 'description')
    list_filter = ('test_category', 'last_update_date', 'created_date')

@admin.register(TestInstruction)
class TestInstructionAdmin(admin.ModelAdmin):
    list_display = ('id', 'test_category', 'instruction_title', 'last_update_date', 'created_date')
    search_fields = ('instruction_title', 'instruction')
    list_filter = ('test_category', 'last_update_date', 'created_date')

@admin.register(AdditionalInstruction)
class AdditionalInstructionAdmin(admin.ModelAdmin):
    list_display = ('id', 'testing_instruction', 'additional_title', 'last_update_date', 'created_date')
    search_fields = ('additional_title', 'additional_description')
    list_filter = ('testing_instruction', 'last_update_date', 'created_date')

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'test_content', 'answer_vars', 'output_time', 'last_update_date', 'created_date')
    search_fields = ('user__email', 'test__question')
    list_filter = ('user', 'test_content', 'last_update_date', 'created_date')

@admin.register(UserStatistic)
class UserStatisticAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'test', 'true_answer_count', 'false_answer_count', 'last_update_date', 'created_date')
    search_fields = ('user__email', 'test__question')
    list_filter = ('user', 'test', 'last_update_date', 'created_date')
