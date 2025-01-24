from django.contrib import admin
from .models import Subject, Graduate, Teacher, Feedback


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ["name"]


@admin.register(Graduate)
class GraduateAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "score", "created_at")
    search_fields = ["first_name", "last_name"]


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "subject", "created_at")
    search_fields = ["first_name", "last_name"]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "phone_number", "created_at")
    search_fields = ["first_name", "last_name", "email"]
