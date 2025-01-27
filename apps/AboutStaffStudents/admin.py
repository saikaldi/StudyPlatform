from django.contrib import admin
from .models import Subject, Graduate, Teacher, Feedback
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

class GraduateAdminForm(forms.ModelForm):
    review = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Отзыв выпускника"
    )
    class Meta:
        model = Graduate
        fields = '__all__'

class FeedbackAdminForm(forms.ModelForm):
    text = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Текст отзыва"
    )
    class Meta:
        model = Feedback
        fields = '__all__'

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    list_display = ['name', 'last_updated', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']
    ordering = ['-created_at']

@admin.register(Graduate)
class GraduateAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    form = GraduateAdminForm
    list_display = ['first_name', 'last_name', 'score', 'last_updated', 'created_at']
    list_filter = ['score', 'last_updated', 'created_at']
    search_fields = ['first_name', 'last_name']
    ordering = ['-created_at']
    
    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="graduates.csv"'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Score', 'Review', 'Last Updated', 'Created At'])
        for obj in queryset:
            writer.writerow([obj.first_name, obj.last_name, obj.score, obj.review, obj.last_updated, obj.created_at])
        return response
    
    export_as_csv.short_description = "Экспорт выбранных выпускников в CSV"

    actions = [export_as_csv]

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    list_display = ['first_name', 'last_name', 'subject', 'last_updated', 'created_at']
    list_filter = ['subject', 'last_updated', 'created_at']
    search_fields = ['first_name', 'last_name', 'subject__name']
    ordering = ['-created_at']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    exclude = ("slug",)
    form = FeedbackAdminForm
    list_display = ['first_name', 'last_name', 'email', 'phone_number', 'last_updated', 'created_at']
    list_filter = ['last_updated', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number']
    ordering = ['-created_at']

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="feedback.csv"'
        writer = csv.writer(response)
        writer.writerow(['First Name', 'Last Name', 'Email', 'Phone Number', 'Text', 'Last Updated', 'Created At'])
        for obj in queryset:
            writer.writerow([obj.first_name, obj.last_name, obj.email, obj.phone_number, obj.text, obj.last_updated, obj.created_at])
        return response
    
    export_as_csv.short_description = "Экспорт выбранных отзывов в CSV"

    actions = [export_as_csv]
