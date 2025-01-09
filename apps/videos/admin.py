from django.contrib import admin
from .models import CategoryVideo, Video, Test, UserAnswer, Result

@admin.register(CategoryVideo)
class CategoryVideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    search_fields = ['name', 'slug']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('subject', 'category', 'is_paid', 'slug')
    list_filter = ('category', 'is_paid')
    search_fields = ['subject', 'description', 'slug']

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('text', 'video', 'is_paid')
    list_filter = ('video', 'is_paid')
    search_fields = ['text', 'video__subject']

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('student', 'question', 'answer', 'is_correct', 'created_data')
    list_filter = ('student', 'created_data')
    search_fields = ['student__username', 'question__text']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'video', 'result_percentage', 'passed', 'created_data')
    list_filter = ('student', 'video', 'passed', 'created_data')
    search_fields = ['student__username', 'video__subject']