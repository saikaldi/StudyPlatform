# Generated by Django 5.1.4 on 2024-12-25 21:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_paid_alter_user_user_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
    ]
