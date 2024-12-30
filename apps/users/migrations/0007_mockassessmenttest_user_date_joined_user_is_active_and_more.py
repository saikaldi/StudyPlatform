# Generated by Django 5.1.4 on 2024-12-29 20:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_user_is_active_remove_user_is_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='MockAssessmentTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=13, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='Введите корректный номер телефона', regex='^\\+?1?\\d{9,13}$')])),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Пробная запись на оценочный тест',
                'verbose_name_plural': 'Пробные записи на оценочные тесты',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True, default=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
