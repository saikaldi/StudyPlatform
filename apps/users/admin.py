from django.contrib import admin
from django.core.mail import send_mail
from .models import User, Profile, EmailConfirmation, MockAssessmentTest
from django.utils import timezone


@admin.action(description="Одобрить статус пользователя")
def approve_user_status(modeladmin, request, queryset):
    for user in queryset:
        if not user.is_status_approved:
            user.is_status_approved = True
            user.is_active = True
            user.save()

            send_mail(
                "Изменение статуса одобрено",
                "Ваш запрос на изменение статуса был одобрен администратором",
                "aktanarynov566@gmail.com",
                [user.email],
                fail_silently=False,
            )

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "user_status", "paid", "is_status_approved", "is_active", "is_staff", "date_joined")
    list_filter = ("user_status", "paid", "is_status_approved", "is_active", "is_staff", "date_joined")
    search_fields = ("email", "first_name", "last_name")
    actions = [approve_user_status]

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name')}),
        ('Статус пользователя', {'fields': ('user_status', 'is_status_approved')}),
        ('Статус оплаты', {'fields': ('paid',)}),
        ('Права и активность', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('date_joined',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    ordering = ('email',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user__first_name', 'user__last_name', 'phone_number', 'address', 'date_of_birth', 'gender')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone_number')
    list_filter = ('gender', 'date_of_birth')

@admin.register(EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'is_expired_display')
    search_fields = ('user__email', 'code')
    list_filter = ('created_at',)

    def is_expired_display(self, obj):
        return "Истек" if obj.is_expired() else "Действителен"

    is_expired_display.short_description = 'Состояние'

@admin.register(MockAssessmentTest)
class MockAssessmentTestAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'created_date', 'last_update_date')
    search_fields = ('first_name', 'last_name', 'phone_number')
    list_filter = ('created_date', 'last_update_date')

    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'phone_number')
        }),
        ('Даты', {
            'fields': ('created_date', 'last_update_date')
        }),
    )
