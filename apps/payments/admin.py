from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.db.models import Sum
from .models import PaymentService, Payment
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

class PaymentServiceAdminForm(forms.ModelForm):
    whatsapp_url = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Ссылка на WhatsApp"
    )
    class Meta:
        model = PaymentService
        fields = '__all__'

@admin.register(PaymentService)
class PaymentServiceAdmin(admin.ModelAdmin):
    form = PaymentServiceAdminForm
    list_display = ('id', 'name_with_logo', 'prop_number', 'full_name', 'whatsapp_link', 'total_payments')
    search_fields = ('payment_service_name', 'prop_number', 'full_name')
    list_filter = ('payment_service_name',)
    fieldsets = (
        (None, {
            'fields': ('payment_service_name',)
        }),
        ('Детали', {
            'fields': ('service_logo', 'qr_code', 'prop_number', 'full_name', 'whatsapp_url'),
        }),
    )

    def name_with_logo(self, obj):
        if obj.service_logo:
            return format_html('<img style="max-height: 30px; max-width: 30px; margin-right: 5px;" src="{}">{}', obj.service_logo.url, obj.payment_service_name)
        return obj.payment_service_name
    
    name_with_logo.short_description = 'Имя сервиса с логотипом'

    def whatsapp_link(self, obj):
        if obj.whatsapp_url:
            return format_html('<a href="{}" target="_blank">WhatsApp</a>', obj.whatsapp_url)
        return '-'
    
    whatsapp_link.short_description = 'WhatsApp'

    def total_payments(self, obj):
        total = Payment.objects.filter(bank=obj).aggregate(total=Sum('amount'))['total']
        return f"{total:.2f} KGS" if total else '0 KGS'
    total_payments.short_description = 'Общая сумма платежей'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user__email', 'bank__payment_service_name', 'amount', 'phone_number', 'status', 'last_update_date', 'created_date')
    list_filter = ('status', 'last_update_date', 'created_date')
    search_fields = ('user__email', 'phone_number', 'slug')
    readonly_fields = ('slug', 'last_update_date', 'created_date')
    date_hierarchy = 'created_date'
    fieldsets = (
        (None, {
            'fields': ('user', 'bank', 'amount', 'phone_number', 'status')
        }),
        ('Мета', {
            'fields': ('slug', 'last_update_date', 'created_date'),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        if not change and not obj.slug:
            unique_string = f"{obj.bank}-{obj.id}"
            obj.slug = slugify(unique_string)
            obj.save()

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if obj and not request.user.is_superuser and obj.user != request.user:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        if obj and not request.user.is_superuser and obj.user != request.user:
            return False
        return True
