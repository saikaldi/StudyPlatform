# Generated by Django 5.1.4 on 2025-01-05 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_alter_test_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='image_a',
            field=models.ImageField(blank=True, null=True, upload_to='question_images/', verbose_name='Изображение варианта А'),
        ),
        migrations.AddField(
            model_name='test',
            name='image_b',
            field=models.ImageField(blank=True, null=True, upload_to='question_images/', verbose_name='Изображение варианта Б'),
        ),
        migrations.AddField(
            model_name='test',
            name='image_c',
            field=models.ImageField(blank=True, null=True, upload_to='question_images/', verbose_name='Изображение варианта В'),
        ),
        migrations.AddField(
            model_name='test',
            name='image_d',
            field=models.ImageField(blank=True, null=True, upload_to='question_images/', verbose_name='Изображение варианта Г'),
        ),
    ]
