# Generated by Django 5.1.4 on 2025-01-24 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("VideoCourse", "0006_subjectcategory_video_subject_category"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                    "categoryName",
                    models.CharField(max_length=100, verbose_name="Название предмета"),
                ),
                (
                    "slug",
                    models.SlugField(
                        blank=True, max_length=100, unique=True, verbose_name="slug"
                    ),
                ),
                (
                    "last_update_date",
                    models.DateTimeField(
                        auto_now=True, verbose_name="Последнее обновление"
                    ),
                ),
                (
                    "created_date",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
            ],
            options={
                "verbose_name": "Название предмета",
                "verbose_name_plural": "1. Название предмета",
            },
        ),
        migrations.AlterModelOptions(
            name="categoryvideo",
            options={
                "verbose_name": "Категория видео",
                "verbose_name_plural": "2. Категории видео",
            },
        ),
        migrations.AlterModelOptions(
            name="subjectcategory",
            options={
                "verbose_name": "Под категория теста",
                "verbose_name_plural": "3. Под категории видео",
            },
        ),
        migrations.AlterModelOptions(
            name="testcontent",
            options={
                "ordering": ["test_order"],
                "verbose_name": "Вопрос теста",
                "verbose_name_plural": "5. Вопросы тестов",
            },
        ),
        migrations.AlterModelOptions(
            name="useranswer",
            options={
                "verbose_name": "Ответ пользователя",
                "verbose_name_plural": "7. Ответы пользователей",
            },
        ),
        migrations.AlterModelOptions(
            name="userstatistic",
            options={
                "verbose_name": "Счет ответов",
                "verbose_name_plural": "6. Счета ответов",
            },
        ),
        migrations.AlterModelOptions(
            name="video",
            options={
                "ordering": ["video_order"],
                "verbose_name": "Видео",
                "verbose_name_plural": "4. Видео",
            },
        ),
    ]
