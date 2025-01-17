from django.contrib import admin
from .models import CategoryVideo, Video, TestContent, UserStatistic, UserAnswer

@admin.register(CategoryVideo)
class CategoryVideoAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'last_update_date', 'created_date')
    search_fields = ['category_name']
    readonly_fields = ['slug', 'last_update_date', 'created_date']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('subject_name', 'video_category', 'video_order', 'is_paid', 'last_update_date', 'created_date')
    list_filter = ('video_category', 'is_paid')
    search_fields = ['subject_name', 'description']
    readonly_fields = ['slug', 'last_update_date', 'created_date']

@admin.register(TestContent)
class TestContentAdmin(admin.ModelAdmin):
    list_display = ('video', 'true_answer', 'test_order', 'last_update_date', 'created_date')
    list_filter = ('video',)
    readonly_fields = ['last_update_date', 'created_date']

@admin.register(UserStatistic)
class UserStatisticAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'true_answer_count', 'false_answer_count', 'last_update_date', 'created_date')
    list_filter = ('user', 'video')
    readonly_fields = ['last_update_date', 'created_date']

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'test_content', 'answer_vars', 'output_time', 'last_update_date', 'created_date')
    list_filter = ('user', 'test_content')
    readonly_fields = ['last_update_date', 'created_date']
