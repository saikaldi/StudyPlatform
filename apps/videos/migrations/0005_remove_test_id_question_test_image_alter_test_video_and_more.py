# Generated by Django 5.1.4 on 2025-01-03 12:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0004_categoryvideo_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test',
            name='id_question',
        ),
        migrations.AddField(
            model_name='test',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='question_images/', verbose_name='Фотография вопроса'),
        ),
        migrations.AlterField(
            model_name='test',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='videos.video', verbose_name='Видео'),
        ),
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='videos.categoryvideo', verbose_name='Категория видео'),
        ),
    ]
