import django_filters
from django_filters import DateFilter, CharFilter, BooleanFilter, ModelChoiceFilter, NumberFilter, ChoiceFilter
from django.conf import settings
from .models import (
    TestCategory,
    SubjectCategory,
    Test,
    TestContent,
    TestFullDescription,
    OkupTushunuu,
    OkupTushunuuText,
    OkupTushunuuQuestion,
    UserStatistic,
    UserAnswer,
)
from django.contrib.auth import get_user_model


class TestCategoryFilter(django_filters.FilterSet):
    test_category_name = CharFilter(field_name='test_category_name', lookup_expr='icontains')
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = TestCategory
        fields = ['test_category_name', 'last_update_date', 'created_date']

class SubjectCategoryFilter(django_filters.FilterSet):
    subject_category_name = CharFilter(field_name='subject_category_name', lookup_expr='icontains')
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = SubjectCategory
        fields = ['subject_category_name', 'last_update_date', 'created_date']

class TestFilter(django_filters.FilterSet):
    test_category = ModelChoiceFilter(field_name='test_category', queryset=TestCategory.objects.all())
    subject_category = ModelChoiceFilter(field_name='subject_category', queryset=SubjectCategory.objects.all())
    title = CharFilter(field_name='title', lookup_expr='icontains')
    first_test = BooleanFilter(field_name='first_test')
    description = CharFilter(field_name='description', lookup_expr='icontains')
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = Test
        fields = ['test_category', 'subject_category', 'title', 'first_test', 'description', 'last_update_date', 'created_date']

class TestContentFilter(django_filters.FilterSet):
    test = ModelChoiceFilter(field_name='test', queryset=Test.objects.all())
    question_number = NumberFilter(field_name='question_number')
    question_text = CharFilter(field_name='question_text', lookup_expr='icontains')
    question_image = CharFilter(field_name='question_image', lookup_expr='icontains')
    additional_questions = CharFilter(field_name='additional_questions', lookup_expr='icontains')
    var_A_image = CharFilter(field_name='var_A_image', lookup_expr='icontains')
    var_B_image = CharFilter(field_name='var_B_image', lookup_expr='icontains')
    var_C_image = CharFilter(field_name='var_C_image', lookup_expr='icontains')
    var_D_image = CharFilter(field_name='var_D_image', lookup_expr='icontains')
    var_A_text = CharFilter(field_name='var_A_text', lookup_expr='icontains')
    var_B_text = CharFilter(field_name='var_B_text', lookup_expr='icontains')
    var_C_text = CharFilter(field_name='var_C_text', lookup_expr='icontains')
    var_D_text = CharFilter(field_name='var_D_text', lookup_expr='icontains')
    true_answer = ChoiceFilter(field_name='true_answer', choices=[('а', 'А'), ('б', 'Б'), ('в', 'В'), ('г', 'Г')])
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = TestContent
        fields = ['test', 'question_number', 'question_text', 'question_image', 'additional_questions',
                  'var_A_image', 'var_B_image', 'var_C_image', 'var_D_image', 
                  'var_A_text', 'var_B_text', 'var_C_text', 'var_D_text', 
                  'true_answer', 'last_update_date', 'created_date']

class TestFullDescriptionFilter(django_filters.FilterSet):
    test_category = ModelChoiceFilter(field_name='test_category', queryset=TestCategory.objects.all())
    description_title = CharFilter(field_name='description_title', lookup_expr='icontains')
    description = CharFilter(field_name='description', lookup_expr='icontains')
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = TestFullDescription
        fields = ['test_category', 'description_title', 'description', 'last_update_date', 'created_date']

class OkupTushunuuFilter(django_filters.FilterSet):
    name = CharFilter(field_name='name', lookup_expr='icontains')
    description = CharFilter(field_name='description', lookup_expr='icontains')
    created_at = DateFilter(field_name='created_at', lookup_expr='date')

    class Meta:
        model = OkupTushunuu
        fields = ['name', 'description', 'created_at']

class OkupTushunuuTextFilter(django_filters.FilterSet):
    test = ModelChoiceFilter(field_name='test', queryset=OkupTushunuu.objects.all())
    question_number = NumberFilter(field_name='question_number')
    title = CharFilter(field_name='title', lookup_expr='icontains')

    class Meta:
        model = OkupTushunuuText
        fields = ['test', 'question_number', 'title']

class OkupTushunuuQuestionFilter(django_filters.FilterSet):
    question = ModelChoiceFilter(field_name='question', queryset=OkupTushunuuText.objects.all())
    question_number = NumberFilter(field_name='question_number')
    question_text = CharFilter(field_name='question_text', lookup_expr='icontains')
    var_A_text = CharFilter(field_name='var_A_text', lookup_expr='icontains')
    var_B_text = CharFilter(field_name='var_B_text', lookup_expr='icontains')
    var_C_text = CharFilter(field_name='var_C_text', lookup_expr='icontains')
    var_D_text = CharFilter(field_name='var_D_text', lookup_expr='icontains')
    true_answer = ChoiceFilter(field_name='true_answer', choices=[('а', 'А'), ('б', 'Б'), ('в', 'В'), ('г', 'Г')])

    class Meta:
        model = OkupTushunuuQuestion
        fields = ['question', 'question_number', 'question_text', 
                  'var_A_text', 'var_B_text', 'var_C_text', 'var_D_text', 'true_answer']

class UserStatisticFilter(django_filters.FilterSet):
    test = ModelChoiceFilter(field_name='test', queryset=Test.objects.all())
    okup_tushunuu = ModelChoiceFilter(field_name='okup_tushunuu', queryset=OkupTushunuu.objects.all())
    user = ModelChoiceFilter(field_name='user', queryset=get_user_model().objects.all())
    true_answer_count = NumberFilter(field_name='true_answer_count')
    false_answer_count = NumberFilter(field_name='false_answer_count')
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = UserStatistic
        fields = ['test', 'okup_tushunuu', 'user', 'true_answer_count', 'false_answer_count', 'last_update_date', 'created_date']

class UserAnswerFilter(django_filters.FilterSet):
    test_content = ModelChoiceFilter(field_name='test_content', queryset=TestContent.objects.all())
    okup_tushunuu_question = ModelChoiceFilter(field_name='okup_tushunuu_question', queryset=OkupTushunuuQuestion.objects.all())
    user = ModelChoiceFilter(field_name='user', queryset=get_user_model().objects.all())
    answer_vars = ChoiceFilter(field_name='answer_vars', choices=[('а', 'А'), ('б', 'Б'), ('в', 'В'), ('г', 'Г')])
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = UserAnswer
        fields = ['test_content', 'okup_tushunuu_question', 'user', 'answer_vars', 'last_update_date', 'created_date']
