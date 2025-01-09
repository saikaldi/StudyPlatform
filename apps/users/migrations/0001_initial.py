import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="MockAssessmentTest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=13,
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Введите корректный номер телефона",
                                regex="^\\+?1?\\d{9,13}$",
                            )
                        ],
                        verbose_name="Номер телефона",
                    ),
                ),
                ("first_name", models.CharField(max_length=50, verbose_name="Имя")),
                ("last_name", models.CharField(max_length=50, verbose_name="Фамилия")),
                (
                    "last_update_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Дата последнего обновления"
                    ),
                ),
            ],
            options={
                "verbose_name": "Пробная запись на оценочный тест",
                "verbose_name_plural": "Пробные записи на оценочные тесты",
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254, unique=True)),
                (
                    "user_status",
                    models.CharField(
                        choices=[
                            ("Менеджер", "Менеджер"),
                            ("Студент", "Студент"),
                            ("Мугалим", "Мугалим"),
                            ("Админ", "Админ"),
                        ],
                        default="Студент",
                        max_length=10,
                    ),
                ),
                (
                    "paid",
                    models.CharField(
                        choices=[
                            ("Не оплачено", "Не оплачено"),
                            ("Оплачено", "Оплачено"),
                        ],
                        default="Не оплачено",
                        max_length=11,
                    ),
                ),
                ("is_status_approved", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=False)),
                (
                    "date_joined",
                    models.DateTimeField(blank=True, default=django.utils.timezone.now),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
        ),
        migrations.CreateModel(
            name="EmailConfirmation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("code", models.CharField(max_length=6)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_used", models.BooleanField(default=False)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Код активации Аккаунта",
                "verbose_name_plural": "Коды активации Аккаунта",
            },
        ),
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "profile_picture",
                    models.ImageField(
                        blank=True, null=True, upload_to="profile_pictures/"
                    ),
                ),
                ("address", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=13,
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                message="Введите корректный номер телефона",
                                regex="^\\+?1?\\d{9,13}$",
                            )
                        ],
                    ),
                ),
                ("date_of_birth", models.DateField(blank=True, null=True)),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("мужской", "Мужской"), ("женский", "Женский")],
                        max_length=10,
                        null=True,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Профиль",
                "verbose_name_plural": "Профили",
            },
        ),
    ]
