from django.contrib import admin
from .models import (
    TestCategory,
    Test,
    TestContent,
    TestFullDescription,
    # TestInstruction,
    UserStatistic,
    UserAnswer,  # AdditionalInstruction
    SubjectCategory
)


@admin.register(TestCategory)
class TestCategoryAdmin(admin.ModelAdmin):
    list_display = ("test_category_name", "last_update_date", "created_date")
    search_fields = ("test_category_name",)
    ordering = ("-created_date",)

@admin.register(SubjectCategory)
class SubjectCategory(admin.ModelAdmin):
    list_display = ("subject_category_name", "last_update_date", "created_date")
    search_fields = ("subject_category_name",)
    ordering = ("-created_date",)

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "test_category",
        'subject_category',
        "first_test",
        "last_update_date",
        "created_date",
    )
    search_fields = ("title",)
    list_filter = ("test_category", "subject_category", "first_test")
    ordering = ("-created_date",)


# @admin.register(TestContent)
# class TestContentAdmin(admin.ModelAdmin):
#     list_display = (
#         "question_number",
#         "question_text",
#         "question_image",
#         "true_answer",
#         "last_update_date",
#         "created_date",
#     )
#     search_fields = ("test__title", "true_answer")
#     # list_editable = ("question_number",)
#     list_filter = ("test__test_category",)
#     ordering = ("test", "question_number")


class Math1Admin(admin.ModelAdmin):

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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(test__title="Математика 1 Болум")


class Math2Admin(admin.ModelAdmin):

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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(test__title="Математика 2 Болум")


class Kyrgyz1Admin(admin.ModelAdmin):

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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(test__title="Кыргыз Тил - Аналогия")


class Kyrgyz2Admin(admin.ModelAdmin):

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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(test__title="Кыргыз Тил - Окуу жана тушунуу")


class Kyrgyz3Admin(admin.ModelAdmin):

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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(test__title="Кыргыз Тил - Грамматика")


# # # Registering proxy models
# # class Math1TestContent(TestContent):

# #     class Meta:
# #         proxy = True
# #         verbose_name = "Математика 1 Болум"
# #         verbose_name_plural = "Математика 1 Болум"


# # class Math2TestContent(TestContent):

# #     class Meta:
# #         proxy = True
# #         verbose_name = "Математика 2 Болум"
# #         verbose_name_plural = "Математика 2 Болум"


# # class Kyrgyz1TestContent(TestContent):

# #     class Meta:
# #         proxy = True
# #         verbose_name = "Кыргыз Тил - Аналогия"
# #         verbose_name_plural = "Кыргыз Тил - Аналогия"


# # class Kyrgyz2TestContent(TestContent):

# #     class Meta:
# #         proxy = True
# #         verbose_name = "Кыргыз Тил - Окуу жана тушунуу"
# #         verbose_name_plural = "Кыргыз Тил - Окуу жана тушунуу"


# # class Kyrgyz3TestContent(TestContent):

# #     class Meta:
# #         proxy = True
# #         verbose_name = "Кыргыз Тил - Грамматика"
# #         verbose_name_plural = "Кыргыз Тил - Грамматика"


# admin.site.register(Math1TestContent, Math1Admin)
# admin.site.register(Math2TestContent, Math2Admin)
# admin.site.register(Kyrgyz1TestContent, Kyrgyz1Admin)
# admin.site.register(Kyrgyz2TestContent, Kyrgyz2Admin)
# admin.site.register(Kyrgyz3TestContent, Kyrgyz3Admin)


@admin.register(TestFullDescription)
class TestFullDescriptionAdmin(admin.ModelAdmin):
    list_display = (
        "test_category",
        "description_title",
        "last_update_date",
        "created_date",
    )
    search_fields = ("description_title",)
    list_filter = ("test_category",)
    ordering = ("-created_date",)


@admin.register(UserStatistic)
class UserStatisticAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "test",
        "true_answer_count",
        "false_answer_count",
        "last_update_date",
        "created_date",
    )
    search_fields = ("user__email", "test__title")
    list_filter = ("test__test_category",)
    ordering = ("-created_date",)


@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "test_content",
        "answer_vars",
        "last_update_date",
        "created_date",
    )
    search_fields = ("user__email", "test_content__test__title")
    list_filter = ("test_content__test__test_category",)
    ordering = ("-created_date",)
