# Generated by Django 5.1.4 on 2025-01-23 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("OrtTest", "0003_kyrgyzokuptushunuuquestion_last_update_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="kyrgyzokuptushunuutext",
            name="text_number",
            field=models.PositiveIntegerField(
                blank=True, null=True, verbose_name="Номер текста"
            ),
        ),
    ]
