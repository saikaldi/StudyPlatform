from django.db import models
from ..users.models import User


def upload_to_test(instance, filename):
    if hasattr(instance, 'test') and instance.test:
        return f'{instance.test.title}/{filename}'
    return f'unknown/{filename}'

class TestCategory(models.Model):
    test_category_name = models.CharField(max_length=52, verbose_name='Название типа теста')
    last_update_date = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.test_category_name
    
    class Meta:
        verbose_name = 'Категория теста'
        verbose_name_plural = 'Категории тестов'

class Test(models.Model):
    test_category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, verbose_name='Категория теста')
    title = models.CharField(max_length=100, verbose_name='Название теста')
    first_test = models.BooleanField(default=False, verbose_name='Обозначение будет ли тест первым бесплатным тестом')
    description = models.TextField(verbose_name='Описание теста')
    background_image = models.ImageField(upload_to='test_background_image/', verbose_name='Фоновое изображение')
    last_update_date = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

class TestContent(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    question = models.TextField(verbose_name='Вопрос')
    var_A = models.ImageField(upload_to=upload_to_test, verbose_name='Вариант ответа \'A\'')
    var_B = models.ImageField(upload_to=upload_to_test, verbose_name='Вариант ответа \'B\'')
    var_C = models.ImageField(upload_to=upload_to_test, verbose_name='Вариант ответа \'C\'')
    var_D = models.ImageField(upload_to=upload_to_test, verbose_name='Вариант ответа \'D\'')
    true_answer = models.CharField(max_length=10, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], verbose_name='Правильный ответ')
    timer = models.PositiveIntegerField(verbose_name='Таймер (в секундах)')
    last_update_date = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.test.test_category.test_category_name} - {self.test.title} - {self.true_answer}'

    class Meta:
        verbose_name = 'Вопрос теста'
        verbose_name_plural = 'Вопросы тестов'

class TestFullDescription(models.Model):
    test_category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, verbose_name='Категория теста')
    description_title = models.CharField(max_length=60, verbose_name='Название описания')
    description = models.TextField(verbose_name='Описание')
    last_update_date = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.test_category.test_category_name} - {self.description_title}'
    
    class Meta:
        verbose_name = 'Подробное описание теста'
        verbose_name_plural = 'Подробные описания тестов'

class TestInstruction(models.Model):
    test_category = models.ForeignKey(TestCategory, on_delete=models.CASCADE, verbose_name='Категория теста')
    instruction_title = models.CharField(max_length=60, verbose_name='Название инструкции')
    instruction = models.TextField(verbose_name='Инструкция')
    last_update_date = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return self.instruction_title

    class Meta:
        verbose_name = 'Инструкция теста'
        verbose_name_plural = 'Инструкции тестов'

class AdditionalInstruction(models.Model):
    testing_instruction = models.ForeignKey(TestInstruction, on_delete=models.CASCADE, verbose_name='Инструкция теста')
    additional_title = models.CharField(max_length=40, verbose_name='Название дополнительной инструкции')
    additional_description = models.TextField(verbose_name='Описание дополнительной инструкции')
    last_update_date = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.testing_instruction} - {self.additional_title}'
    
    class Meta:
        verbose_name = 'Дополнительная инструкция'
        verbose_name_plural = 'Дополнительные инструкции'

class UserStatistic(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    true_answer_count = models.PositiveIntegerField(default=0, verbose_name='Количество правильных ответов')
    false_answer_count = models.PositiveIntegerField(default=0, verbose_name='Количество неправильных ответов')
    last_update_date = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.user.email} - {self.test.title} - правильные ответы: {self.true_answer_count} - неправильные ответы: {self.false_answer_count}'

    class Meta:
        verbose_name = 'Счет ответов'
        verbose_name_plural = 'Счета ответов'
        unique_together = ('test', 'user')

class UserAnswer(models.Model):
    test_content = models.ForeignKey(TestContent, on_delete=models.CASCADE, verbose_name='Тест контент')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    answer_vars = models.CharField(max_length=1, choices=[('a', 'A'), ('b', 'B'), ('c', 'C'), ('d', 'D')], verbose_name='Ответ')
    output_time = models.PositiveIntegerField(default=1, verbose_name='Время ответа (в секундах)')
    last_update_date = models.DateTimeField(auto_now=True, verbose_name='Последнее обновление')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.user.email} - {self.test_content.test.title}'
    
    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'
