# Generated by Django 5.1.4 on 2025-01-27 12:38

import apps.VideoCourse.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('VideoCourse', '0009_rename_categoryname_category_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='testcontent',
            name='var_E_image',
            field=models.ImageField(blank=True, null=True, upload_to=apps.VideoCourse.models.upload_to_test, verbose_name="Вариант ответа 'Д' (В файловом варианте)"),
        ),
        migrations.AddField(
            model_name='testcontent',
            name='var_E_text',
            field=models.TextField(blank=True, null=True, verbose_name="Вариант ответа 'Д' (В текстовом варианте)"),
        ),
        migrations.AlterField(
            model_name='testcontent',
            name='true_answer',
            field=models.CharField(choices=[('а', 'А'), ('б', 'Б'), ('в', 'В'), ('г', 'Г'), ('д', 'Д')], max_length=10, verbose_name='Правильный ответ'),
        ),
        migrations.AlterField(
            model_name='testcontent',
            name='var_A_text',
            field=models.TextField(blank=True, null=True, verbose_name="Вариант ответа 'А' (В текстовом варианте)"),
        ),
        migrations.AlterField(
            model_name='testcontent',
            name='var_B_image',
            field=models.ImageField(blank=True, null=True, upload_to=apps.VideoCourse.models.upload_to_test, verbose_name="Вариант ответа 'Б' (В файловом варианте)"),
        ),
        migrations.AlterField(
            model_name='testcontent',
            name='var_B_text',
            field=models.TextField(blank=True, null=True, verbose_name="Вариант ответа 'Б' (В текстовом варианте)"),
        ),
        migrations.AlterField(
            model_name='testcontent',
            name='var_C_image',
            field=models.ImageField(blank=True, null=True, upload_to=apps.VideoCourse.models.upload_to_test, verbose_name="Вариант ответа 'В' (В файловом варианте)"),
        ),
        migrations.AlterField(
            model_name='testcontent',
            name='var_C_text',
            field=models.TextField(blank=True, null=True, verbose_name="Вариант ответа 'В' (В текстовом варианте)"),
        ),
        migrations.AlterField(
            model_name='testcontent',
            name='var_D_image',
            field=models.ImageField(blank=True, null=True, upload_to=apps.VideoCourse.models.upload_to_test, verbose_name="Вариант ответа 'Г' (В файловом варианте)"),
        ),
        migrations.AlterField(
            model_name='testcontent',
            name='var_D_text',
            field=models.TextField(blank=True, null=True, verbose_name="Вариант ответа 'Г' (В текстовом варианте)"),
        ),
    ]
