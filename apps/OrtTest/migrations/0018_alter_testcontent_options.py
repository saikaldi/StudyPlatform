from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("OrtTest", "0017_remove_useranswer_test_useranswer_test_content_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="testcontent",
            options={
                "verbose_name": "Вопрос теста",
                "verbose_name_plural": "Вопросы тестов",
            },
        ),
    ]
