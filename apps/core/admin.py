from django.contrib import admin
from .models import Graduate, Feedback, AbountTeacher, TeacherType
# Register your models here.

class GraduateAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname',  'score', 'created_data')
    prepopulated_fields = {'slug': ('name', 'lastname')}
    

class AbountTeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname', 'teacher_type', 'created_data')
    prepopulated_fields = {'slug': ('name', 'lastname')}
    
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'lastname', 'gmail', 'phone_number', 'created_data')
    prepopulated_fields = {'slug': ('name', 'lastname')}
    
class TeacherTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'created_data')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(TeacherType, TeacherTypeAdmin)
admin.site.register(Graduate, GraduateAdmin)
admin.site.register(AbountTeacher, AbountTeacherAdmin)
admin.site.register(Feedback, FeedbackAdmin)