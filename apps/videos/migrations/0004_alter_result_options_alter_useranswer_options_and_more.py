# Generated by Django 5.1.4 on 2025-01-08 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_alter_categoryvideo_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ['-created_data'], 'verbose_name': 'Результат', 'verbose_name_plural': 'Результаты'},
        ),
        migrations.AlterModelOptions(
            name='useranswer',
            options={'ordering': ['-student', '-created_data'], 'verbose_name': 'Ответ', 'verbose_name_plural': 'Ответы'},
        ),
        migrations.AlterField(
            model_name='test',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Текст вопроса'),
        ),
    ]
