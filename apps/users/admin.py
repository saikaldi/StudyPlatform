from django.contrib import admin
from django.core.mail import send_mail
from .models import User, Profile, EmailConfirmation
from django.utils import timezone
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class ProfileAdminForm(forms.ModelForm):
    address = forms.CharField(
        widget=CKEditorUploadingWidget(),
        label="Адрес пользователя"
    )
    class Meta:
        model = Profile
        fields = '__all__'

@admin.action(description=_("Одобрить статус пользователя"))
def approve_user_status(modeladmin, request, queryset):
    with transaction.atomic():
        for user in queryset:
            if not user.is_status_approved:
                user.is_status_approved = True
                user.is_active = True
                user.save()

                try:
                    send_mail(
                        _(f"Изменение статуса одобрено"),
                        _(f"Ваш запрос на изменение статуса был одобрен администратором"),
                        "aktanarynov566@gmail.com",
                        [user.email],
                        fail_silently=False,
                    )
                except Exception as e:
                    modeladmin.message_user(
                        request,
                        _(f"Ошибка отправки письма пользователю {user.email}: {str(e)}"),
                        level="error",
                    )

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "user_status",
        "paid",
        "is_status_approved",
        "is_active",
        "is_staff",
        "date_joined",
    )
    list_filter = (
        "user_status",
        "paid",
        "is_status_approved",
        "is_active",
        "is_staff",
        "date_joined",
    )
    search_fields = ("email", "first_name", "last_name")
    actions = [approve_user_status]

    fieldsets = (
        (None, {"fields": ("email", "password")} ),
        (_("Личная информация"), {"fields": ("first_name", "last_name")}),
        (_("Статус пользователя"), {"fields": ("user_status", "is_status_approved")}),
        (_("Статус оплаты"), {"fields": ("paid",)}),
        (
            _(f"Права и активность"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Даты"), {"fields": ("date_joined",)}),
    )

    ordering = ("email",)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    form = ProfileAdminForm
    list_display = (
        "user",
        "get_first_name",
        "get_last_name",
        "phone_number",
        "address",
        "date_of_birth",
        "gender",
    )
    search_fields = ("user__email", "user__first_name", "user__last_name", "phone_number")
    list_filter = ("gender", "date_of_birth")

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.short_description = _(f"Имя")

    def get_last_name(self, obj):
        return obj.user.last_name

    get_last_name.short_description = _(f"Фамилия")

@admin.register(EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "created_at", "is_expired_display")
    search_fields = ("user__email", "code")
    list_filter = ("created_at",)

    def is_expired_display(self, obj):
        return _(f"Истек") if obj.is_expired() else _(f"Действителен")

    is_expired_display.short_description = _(f"Состояние")

# @admin.register(MockAssessmentTest)
# class MockAssessmentTestAdmin(admin.ModelAdmin):
#     list_display = (
#         "first_name",
#         "last_name",
#         "phone_number",
#         "created_date",
#         "formatted_last_update_date",
#     )
#     search_fields = ("first_name", "last_name", "phone_number")
#     list_filter = ("created_date", "last_update_date")

#     fieldsets = (
#         (None, {"fields": ("first_name", "last_name", "phone_number")} ),
#         (_("Даты"), {"fields": ("created_date", "last_update_date")}),
#     )
#     readonly_fields = ("last_update_date", "created_date")

#     def formatted_last_update_date(self, obj):
#         return (
#             obj.last_update_date.strftime("%d.%m.%Y %H:%M")
#             if obj.last_update_date
#             else _(f"Не обновлялся")
#         )

#     formatted_last_update_date.short_description = _(f"Последнее обновление")
