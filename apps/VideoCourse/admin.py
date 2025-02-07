from django.contrib import admin
from .models import (
    CategoryVideo,
    Video,
    TestContent,
    UserStatistic,
    UserAnswer,
    SubjectCategory,
    Category,
)
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class VideoAdminForm(forms.ModelForm):
    description = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Описание видео"
    )
    class Meta:
        model = Video
        fields = '__all__'

class TestContentAdminForm(forms.ModelForm):
    question_text = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Текст вопроса",
        required=False
    )
    additional_questions = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Дополнительные вопросы",
        required=False
    )
    var_A_text = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Вариант ответа A",
        required=False
    )
    var_B_text = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Вариант ответа Б",
        required=False
    )
    var_C_text = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Вариант ответа В",
        required=False
    )
    var_D_text = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Вариант ответа Г",
        required=False
    )
    var_E_text = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Вариант ответа Д",
        required=False
    )
    class Meta:
        model = TestContent
        fields = '__all__'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "last_update_date", "created_date")
    search_fields = ["category_name"]
    readonly_fields = ["slug", "last_update_date", "created_date"]

@admin.register(CategoryVideo)
class CategoryVideoAdmin(admin.ModelAdmin):
    list_display = ("category_name", "last_update_date", "created_date")
    search_fields = ["category_name"]
    readonly_fields = ["slug", "last_update_date", "created_date"]

@admin.register(SubjectCategory)
class SubjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("subject_category_name", "last_update_date", "created_date")
    search_fields = ("subject_category_name",)
    ordering = ("-created_date",)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    form = VideoAdminForm
    list_display = (
        "subject_name",
        "video_category",
        "subject_category",
        "video_order",
        "is_paid",
        "last_update_date",
        "created_date",
    )
    list_filter = ("video_category", "subject_category", "is_paid")
    search_fields = ["subject_name", "description"]
    readonly_fields = ["slug", "last_update_date", "created_date"]

@admin.register(TestContent)
class TestContentAdmin(admin.ModelAdmin):
    form = TestContentAdminForm
    list_display = (
        "video",
        "true_answer",
        "test_order",
        "last_update_date",
        "created_date",
    )
    list_filter = ("video",)
    readonly_fields = ["last_update_date", "created_date"]

@admin.register(UserStatistic)
class UserStatisticAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "video",
        "true_answer_count",
        "false_answer_count",
        "accuracy_percentage",
        "last_update_date",
        "created_date",
    )
    list_filter = ("user", "video")
    readonly_fields = ["last_update_date", "created_date", "accuracy_percentage"]

    def save_model(self, request, obj, form, change):
        obj.update_accuracy()
        super().save_model(request, obj, form, change)

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "test_content",
        "answer_vars",
        "output_time",
        "last_update_date",
        "created_date",
    )
    list_filter = ("user", "test_content")
    readonly_fields = ["last_update_date", "created_date"]
