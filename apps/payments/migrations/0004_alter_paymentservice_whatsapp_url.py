# Generated by Django 5.1.4 on 2025-01-08 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_paymentservice_delete_paymentmethod_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentservice',
            name='whatsapp_url',
            field=models.TextField(blank=True, null=True, verbose_name='Ссылка на WhatsApp'),
        ),
    ]
