from django.contrib import admin
from .models import CategoryVideo, Video, Test, UserAnswer, Result

@admin.register(CategoryVideo)
class CategoryVideoAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'slug')
    list_filter = ('parent',)
    search_fields = ['name', 'slug']
    
    def parent_name(self, obj):
        return obj.parent.name if obj.parent else "None"
    
    parent_name.short_description = 'Родительская категория'

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('subject', 'category_name', 'is_paid', 'slug', 'created_data')
    list_filter = ('category', 'is_paid', 'created_data')
    search_fields = ['subject', 'description', 'slug']
    
    def category_name(self, obj):
        return obj.category.name if obj.category else "None"
    
    category_name.short_description = 'Категория'

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('text_preview', 'video_subject', 'is_paid', 'created_data')
    list_filter = ('video', 'is_paid', 'created_data')
    search_fields = ['text', 'video__subject']
    
    def text_preview(self, obj):
        return obj.text[:50] + "..." if len(obj.text) > 50 else obj.text
    
    text_preview.short_description = 'Вопрос'
    
    def video_subject(self, obj):
        return obj.video.subject
    
    video_subject.short_description = 'Предмет'

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('student_email', 'question_text', 'answer', 'is_correct', 'created_data')
    list_filter = ('student', 'created_data')
    search_fields = ['student__email', 'question__text']
    
    def student_email(self, obj):
        return obj.student.email
    
    student_email.short_description = 'Студент'
    
    def question_text(self, obj):
        return obj.question.text[:50] + "..." if len(obj.question.text) > 50 else obj.question.text
    
    question_text.short_description = 'Вопрос'

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student_username', 'video_subject', 'result_percentage', 'passed', 'created_data')
    list_filter = ('student', 'video', 'passed', 'created_data')
    search_fields = ['student__username', 'video__subject']
    
    def student_username(self, obj):
        return obj.student.username
    
    student_username.short_description = 'Студент'
    
    def video_subject(self, obj):
        return obj.video.subject
    
    video_subject.short_description = 'Предмет'
