import django_filters
from django_filters import CharFilter, BooleanFilter, DateFilter, NumberFilter, ChoiceFilter, ModelChoiceFilter
from .models import *
from django.contrib.auth import get_user_model


class CategoryFilter(django_filters.FilterSet):
    category_name = CharFilter(field_name='category_name', lookup_expr='icontains')
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = Category
        fields = ['category_name', 'last_update_date', 'created_date']

class CategoryVideoFilter(django_filters.FilterSet):
    category_name = CharFilter(field_name='category_name', lookup_expr='icontains')
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = CategoryVideo
        fields = ['category_name', 'last_update_date', 'created_date']

class SubjectCategoryFilter(django_filters.FilterSet):
    subject_category_name = CharFilter(field_name='subject_category_name', lookup_expr='icontains')
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = SubjectCategory
        fields = ['subject_category_name', 'last_update_date', 'created_date']

class VideoFilter(django_filters.FilterSet):
    category = ModelChoiceFilter(field_name='category', queryset=Category.objects.all())
    video_category = ModelChoiceFilter(field_name='video_category', queryset=CategoryVideo.objects.all())
    subject_category = ModelChoiceFilter(field_name='subject_category', queryset=SubjectCategory.objects.all())
    subject_name = CharFilter(field_name='subject_name', lookup_expr='icontains')
    description = CharFilter(field_name='description', lookup_expr='icontains')
    video_url = CharFilter(field_name='video_url', lookup_expr='icontains')
    video_order = NumberFilter(field_name='video_order')
    is_paid = BooleanFilter(field_name='is_paid')
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = Video
        fields = [
            'category', 'video_category', 'subject_category', 'subject_name', 'description',
            'video_url', 'video_order', 'is_paid', 'last_update_date', 'created_date'
        ]

class TestContentFilter(django_filters.FilterSet):
    video = ModelChoiceFilter(field_name='video', queryset=Video.objects.all())
    question_text = CharFilter(field_name='question_text', lookup_expr='icontains')
    true_answer = ChoiceFilter(field_name='true_answer', choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')])
    test_order = NumberFilter(field_name='test_order')
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = TestContent
        fields = ['video', 'question_text', 'true_answer', 'test_order', 'last_update_date', 'created_date']

class UserStatisticFilter(django_filters.FilterSet):
    video = ModelChoiceFilter(field_name='video', queryset=Video.objects.all())
    user = ModelChoiceFilter(field_name='user', queryset=get_user_model().objects.all())
    true_answer_count = NumberFilter(field_name='true_answer_count')
    false_answer_count = NumberFilter(field_name='false_answer_count')
    accuracy_percentage = NumberFilter(field_name='accuracy_percentage')
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = UserStatistic
        fields = ['video', 'user', 'true_answer_count', 'false_answer_count', 'accuracy_percentage', 'last_update_date', 'created_date']

class UserAnswerFilter(django_filters.FilterSet):
    test_content = ModelChoiceFilter(field_name='test_content', queryset=TestContent.objects.all())
    user = ModelChoiceFilter(field_name='user', queryset=get_user_model().objects.all())
    answer_vars = ChoiceFilter(field_name='answer_vars', choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')])
    output_time = NumberFilter(field_name='output_time')
    last_update_date = DateFilter(field_name='last_update_date', lookup_expr='date')
    created_date = DateFilter(field_name='created_date', lookup_expr='date')

    class Meta:
        model = UserAnswer
        fields = ['test_content', 'user', 'answer_vars', 'output_time', 'last_update_date', 'created_date']
