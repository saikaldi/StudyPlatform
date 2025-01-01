from django.contrib import admin
from .models import Graduate, Feedback, AbountTeacher
# Register your models here.

class GraduateAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname', 'image', 'score', 'review', 'slug', 'created_data')
    prepopulated_fields = {'slug': ('name', 'lastname')}
    

class AbountTeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname', 'teacher_type', 'image', 'slug', 'created_data')
    prepopulated_fields = {'slug': ('name', 'lastname')}
    
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname', 'gmail', 'phone_number', 'text', 'slug', 'created_data')
    prepopulated_fields = {'slug': ('name', 'lastname')}



admin.site.register(Graduate, GraduateAdmin)
admin.site.register(AbountTeacher, AbountTeacherAdmin)
admin.site.register(Feedback, FeedbackAdmin)