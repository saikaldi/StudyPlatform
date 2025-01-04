# Generated by Django 5.1.4 on 2025-01-03 16:31

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_user_first_test_passed'),
    ]

    operations = [
        migrations.AddField(
            model_name='mockassessmenttest',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mockassessmenttest',
            name='last_update_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='last_update_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
