from django.contrib import admin
from .models import PaymentService, Payment
from django.utils.text import slugify


class PaymentServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'payment_service_name', 'prop_number', 'full_name')
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

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'bank', 'amount', 'phone_number', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'bank', 'created_at', 'updated_at')
    search_fields = ('user__username', 'phone_number', 'slug')
    readonly_fields = ('slug', 'created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'bank', 'amount', 'phone_number', 'status')
        }),
        ('Мета', {
            'fields': ('slug', 'created_at', 'updated_at'),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        if not change and not obj.slug:
            unique_string = f"{obj.bank}-{obj.id}"
            obj.slug = slugify(unique_string)
            obj.save()

admin.site.register(PaymentService, PaymentServiceAdmin)
admin.site.register(Payment, PaymentAdmin)
