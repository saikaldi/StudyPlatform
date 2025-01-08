from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),  # Зависимость от первой миграции
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],  # Оставить базу без изменений
            state_operations=[],     # Отметить миграцию как выполненную
        ),
    ]
