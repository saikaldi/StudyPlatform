from django.contrib import admin
from .models import (
    TestCategory,
    Test,
    TestContent,
    TestFullDescription,
    UserStatistic,
    UserAnswer,
    SubjectCategory,
    OkupTushunuu,
    OkupTushunuuText,
    OkupTushunuuQuestion,
)
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class TestForm(forms.ModelForm):
    description = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Описание теста"
    )
    class Meta:
        model = Test
        fields = '__all__'

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "test_category",
        "subject_category",
        "first_test",
        "last_update_date",
        "created_date",
    )
    search_fields = ("title",)
    list_filter = ("test_category", "subject_category", "first_test")
    ordering = ("-created_date",)
    form = TestForm

class TestContentForm(forms.ModelForm):
    question_text = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Текст вопроса",
        required=False
    )
    additional_questions = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Дополнительный текст к вопросу",
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

@admin.register(TestContent)
class TestContentAdmin(admin.ModelAdmin):
    list_display = (
        "question_number",
        "question_text",
        "question_image",
        "true_answer",
        "last_update_date",
        "created_date",
    )
    search_fields = ("test__title", "true_answer")
    list_filter = ("test__test_category",)
    ordering = ("test", "question_number")
    form = TestContentForm

class TestFullDescriptionAdminForm(forms.ModelForm):
    # description = forms.CharField(
    #     widget=CKEditorUploadingWidget(),
    #     label="Подробное описание"
    # )
    class Meta:
        model = TestFullDescription
        fields = '__all__'

@admin.register(TestFullDescription)
class TestFullDescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "test_category",
        "description_title",
        "last_update_date",
        "created_date",
    )
    form = TestFullDescriptionAdminForm
    search_fields = ("description_title",)
    list_filter = ("test_category",)
    ordering = ("-created_date",)

class OkupTushunuuForm(forms.ModelForm):
    description = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Описание теста"
    )
    class Meta:
        model = OkupTushunuu
        fields = '__all__'

@admin.register(OkupTushunuu)
class OkupTushunuuAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_at")
    search_fields = ("name", "description")
    list_filter = ("created_at",)
    form = OkupTushunuuForm

class OkupTushunuuQuestionForm(forms.ModelForm):
    question_text = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Текст вопроса"
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
        model = OkupTushunuuQuestion
        fields = '__all__'

@admin.register(OkupTushunuuQuestion)
class OkupTushunuuQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "question", "true_answer", "question_number")
    search_fields = ("question_text", "question__title")
    list_filter = ("true_answer",)
    form = OkupTushunuuQuestionForm

@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ("test_category_name", "last_update_date", "created_date")
    search_fields = ("test_category_name",)
    ordering = ("-created_date",)

@admin.register(SubjectCategory)
class SubjectCategoryAdmin(admin.ModelAdmin):
    list_display = ("subject_category_name", "last_update_date", "created_date")
    search_fields = ("subject_category_name",)
    ordering = ("-created_date",)

@admin.register(UserStatistic)
class UserStatisticAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "test",
        "okup_tushunuu",
        "true_answer_count",
        "false_answer_count",
        "last_update_date",
        "created_date",
    )
    search_fields = ("user__email", "test__title", "okup_tushunuu__name")
    list_filter = ("last_update_date", "created_date")

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "okup_tushunuu_question",
        "test_content",
        "answer_vars",
        "last_update_date",
        "created_date",
    )
    search_fields = (
        "user__email",
        "okup_tushunuu_question__question_text",
        "test_content__test__title",
    )
    list_filter = ("last_update_date", "created_date")

@admin.register(OkupTushunuuText)
class OkupTushunuuTextAdmin(admin.ModelAdmin):
    list_display = ("title", "test", "text_file", "question_number")
    search_fields = ("title", "test__name")
    list_filter = ("test",)
