from django.contrib import admin
from .models import (
    TestCategory, Test, TestContent, TestFullDescription,
    TestInstruction, UserStatistic, UserAnswer #AdditionalInstruction
)

@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ('test_category_name', 'last_update_date', 'created_date')
    search_fields = ('test_category_name',)
    ordering = ('-created_date',)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'test_category', 'first_test', 'last_update_date', 'created_date')
    search_fields = ('title',)
    list_filter = ('test_category', 'first_test')
    ordering = ('-created_date',)


@admin.register(TestContent)
class TestContentAdmin(admin.ModelAdmin):
    list_display = ('test', 'true_answer', 'last_update_date', 'created_date')
    search_fields = ('test__title', 'true_answer')
    list_filter = ('test__test_category',)
    ordering = ('-created_date',)


@admin.register(TestFullDescription)
class TestFullDescriptionAdmin(admin.ModelAdmin):
    list_display = ('test_category', 'description_title', 'last_update_date', 'created_date')
    search_fields = ('description_title',)
    list_filter = ('test_category',)
    ordering = ('-created_date',)


@admin.register(TestInstruction)
class TestInstructionAdmin(admin.ModelAdmin):
    list_display = ('test_category', 'instruction_title', 'last_update_date', 'created_date')
    search_fields = ('instruction_title',)
    list_filter = ('test_category',)
    ordering = ('-created_date',)


# @admin.register(AdditionalInstruction)
# class AdditionalInstructionAdmin(admin.ModelAdmin):
#     list_display = ('testing_instruction', 'additional_title', 'last_update_date', 'created_date')
#     search_fields = ('additional_title',)
#     list_filter = ('testing_instruction__test_category',)
#     ordering = ('-created_date',)


@admin.register(UserStatistic)
class UserStatisticAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'true_answer_count', 'false_answer_count', 'last_update_date', 'created_date')
    search_fields = ('user__email', 'test__title')
    list_filter = ('test__test_category',)
    ordering = ('-created_date',)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'test_content', 'answer_vars', 'output_time', 'last_update_date', 'created_date')
    search_fields = ('user__email', 'test_content__test__title')
    list_filter = ('test_content__test__test_category',)
    ordering = ('-created_date',)
