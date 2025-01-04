# Generated by Django 5.1.4 on 2025-01-04 13:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OrtTest', '0016_rename_testing_instruction_fk_additionalinstruction_testing_instruction_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useranswer',
            name='test',
        ),
        migrations.AddField(
            model_name='useranswer',
            name='test_content',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='OrtTest.testcontent', verbose_name='Тест контент'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userstatistic',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OrtTest.test', verbose_name='Тест'),
        ),
    ]
