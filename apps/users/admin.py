from django.contrib import admin
from .models import User, Profile, EmailConfirmation
from django.core.mail import send_mail


@admin.action(description="Одобрить статус пользователя")
def approve_user_status(modeladmin, request, queryset):
    for user in queryset:
        if not user.is_status_approved:
            user.is_status_approved = True
            user.is_active = True
            user.save()

            # Отправляем уведомление на email пользователя
            send_mail(
                'Изменение статуса одобрено',
                'Ваш запрос на изменение статуса был одобрен администратором',
                'aktanarynov566@gmail.com',
                [user.email],
                fail_silently=False,
            )

class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'user_status', 'is_status_approved')
    actions = [approve_user_status]
    search_fields = ('email',)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user__first_name', 'user__last_name', 'date_of_birth', 'gender')                       # Поля для отображения в списке
    search_fields = ('user__email', 'user__first_name', 'user__last_name')                                          # Поиск по email пользователя и имени
    list_filter = ('gender', 'date_of_birth')                                                                       # Фильтрация по полу и дате рождения

class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'is_expired')                                                     # Поля для отображения в списке
    search_fields = ('user__email', 'code')                                                                         # Поиск по email пользователя и коду
    list_filter = ('created_at',)                                                                                   # Фильтрация по дате создания кода

    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True                                                                                       # Отображение как иконки

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(EmailConfirmation, EmailConfirmationAdmin)
