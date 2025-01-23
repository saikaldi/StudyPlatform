# Generated by Django 5.1.4 on 2025-01-23 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("OrtTest", "0033_okuptushunuu_okuptushunuuquestion_okuptushunuutext_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="okuptushunuu",
            options={
                "verbose_name": "Окуп тушунуу",
                "verbose_name_plural": "5. Окуп тушунуу",
            },
        ),
        migrations.AlterModelOptions(
            name="okuptushunuuquestion",
            options={
                "verbose_name": "Вопрос Окуп тушунуу",
                "verbose_name_plural": "7. Вопросы Окуп тушунуу",
            },
        ),
        migrations.AlterModelOptions(
            name="okuptushunuutext",
            options={
                "verbose_name": "Текст - Окуп тушунуу",
                "verbose_name_plural": "6. Тексты - Окуп тушунуу",
            },
        ),
        migrations.AlterModelOptions(
            name="testcategory",
            options={
                "verbose_name": "Категория предмета",
                "verbose_name_plural": "1. Категории предметов",
            },
        ),
        migrations.AlterModelOptions(
            name="useranswer",
            options={
                "verbose_name": "Ответ пользователя",
                "verbose_name_plural": "8. Ответы пользователей",
            },
        ),
        migrations.AlterModelOptions(
            name="userstatistic",
            options={
                "verbose_name": "Счет ответов",
                "verbose_name_plural": "9. Счета ответов",
            },
        ),
        migrations.AlterField(
            model_name="okuptushunuutext",
            name="question_number",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Номер текста"
            ),
        ),
    ]
