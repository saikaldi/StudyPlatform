# Generated by Django 5.1.4 on 2025-01-04 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, unique=True),
        ),
    ]
