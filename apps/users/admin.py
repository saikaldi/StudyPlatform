from django.contrib import admin
from .models import User, Profile, EmailConfirmation


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'is_staff')  # Поля для отображения в списке
    search_fields = ('email',)  # Поиск по email
    list_filter = ('is_active', 'is_staff')  # Фильтрация по активному статусу и доступу к админке

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user__first_name', 'user__last_name', 'date_of_birth', 'gender')  # Поля для отображения в списке
    search_fields = ('user__email', 'user__first_name', 'user__last_name')  # Поиск по email пользователя и имени
    list_filter = ('gender', 'date_of_birth')  # Фильтрация по полу и дате рождения

class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'is_expired')  # Поля для отображения в списке
    search_fields = ('user__email', 'code')  # Поиск по email пользователя и коду
    list_filter = ('created_at',)  # Фильтрация по дате создания кода

    def is_expired(self, obj):
        return obj.is_expired()
    is_expired.boolean = True  # Отображение как иконки

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(EmailConfirmation, EmailConfirmationAdmin)
