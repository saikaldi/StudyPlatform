from django.contrib import admin
from .models import Subject, Graduate, Teacher, Feedback


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    exclude = ("slug",)

@admin.register(Graduate)
class GraduateAdmin(admin.ModelAdmin):
    exclude = ("slug",)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    exclude = ("slug",)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    exclude = ("slug",)
 