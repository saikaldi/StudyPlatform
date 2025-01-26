import django_filters
from .models import Subject, Graduate, Teacher, Feedback


class SubjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    slug = django_filters.CharFilter(field_name='slug', lookup_expr='icontains')
    last_updated_lte = django_filters.DateTimeFilter(field_name='last_updated', lookup_expr='lte')
    last_updated_gte = django_filters.DateTimeFilter(field_name='last_updated', lookup_expr='gte')
    created_at_lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    created_at_gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')

    class Meta:
        model = Subject
        fields = ['name', 'slug', 'last_updated', 'created_at']

class GraduateFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    score_lte = django_filters.NumberFilter(field_name='score', lookup_expr='lte')
    score_gte = django_filters.NumberFilter(field_name='score', lookup_expr='gte')
    slug = django_filters.CharFilter(field_name='slug', lookup_expr='icontains')
    last_updated_lte = django_filters.DateTimeFilter(field_name='last_updated', lookup_expr='lte')
    last_updated_gte = django_filters.DateTimeFilter(field_name='last_updated', lookup_expr='gte')
    created_at_lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    created_at_gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')

    class Meta:
        model = Graduate
        fields = ['first_name', 'last_name', 'score', 'slug', 'last_updated', 'created_at']

class TeacherFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    subject = django_filters.ModelChoiceFilter(field_name='subject', queryset=Subject.objects.all())
    slug = django_filters.CharFilter(field_name='slug', lookup_expr='icontains')
    last_updated_lte = django_filters.DateTimeFilter(field_name='last_updated', lookup_expr='lte')
    last_updated_gte = django_filters.DateTimeFilter(field_name='last_updated', lookup_expr='gte')
    created_at_lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    created_at_gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'subject', 'slug', 'last_updated', 'created_at']

class FeedbackFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    phone_number = django_filters.CharFilter(field_name='phone_number', lookup_expr='icontains')
    slug = django_filters.CharFilter(field_name='slug', lookup_expr='icontains')
    last_updated_lte = django_filters.DateTimeFilter(field_name='last_updated', lookup_expr='lte')
    last_updated_gte = django_filters.DateTimeFilter(field_name='last_updated', lookup_expr='gte')
    created_at_lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    created_at_gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')

    class Meta:
        model = Feedback
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'slug', 'last_updated', 'created_at']
