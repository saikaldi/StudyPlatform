from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError


def upload_to_test(instance, filename):
    if hasattr(instance, "test") and instance.test:
        return f"{instance.test.test_name}/{filename}"
    return f"unknown/{filename}"

class Test(models.Model):
    test_name = models.CharField(max_length=100, verbose_name='Название пробного теста')
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.test_name

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

class TestContent(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    question_number = models.PositiveIntegerField(
        verbose_name="Порядковый номер вопроса", blank=True, null=True
    )
    question_text = models.TextField(
        verbose_name="Вопрос в текстовом формате", blank=True, null=True
    )
    question_image = models.ImageField(
        verbose_name="Вопрос в файловом формате", blank=True, null=True
    )
    additional_questions = models.TextField(
        verbose_name="Дополнительный текст к вопросу", blank=True, null=True
    )
    var_A_image = models.ImageField(
        upload_to=upload_to_test,
        verbose_name="Вариант ответа 'A' (В файловом варианте)",
        blank=True,
        null=True,
    )
    var_B_image = models.ImageField(
        upload_to=upload_to_test,
        verbose_name="Вариант ответа 'Б' (В файловом варианте)",
        blank=True,
        null=True,
    )
    var_C_image = models.ImageField(
        upload_to=upload_to_test,
        verbose_name="Вариант ответа 'В' (В файловом варианте)",
        blank=True,
        null=True,
    )
    var_D_image = models.ImageField(
        upload_to=upload_to_test,
        verbose_name="Вариант ответа 'Г' (В файловом варианте)",
        blank=True,
        null=True,
    )
    var_E_image = models.ImageField(
        upload_to=upload_to_test,
        verbose_name="Вариант ответа 'Д' (В файловом варианте)",
        blank=True,
        null=True,
    )
    var_A_text = models.TextField(
        verbose_name="Вариант ответа 'А' (В текстовом варианте)", blank=True, null=True
    )
    var_B_text = models.TextField(
        verbose_name="Вариант ответа 'Б' (В текстовом варианте)", blank=True, null=True
    )
    var_C_text = models.TextField(
        verbose_name="Вариант ответа 'В' (В текстовом варианте)", blank=True, null=True
    )
    var_D_text = models.TextField(
        verbose_name="Вариант ответа 'Г' (В текстовом варианте)", blank=True, null=True
    )
    var_E_text = models.TextField(
        verbose_name="Вариант ответа 'Д' (В текстовом варианте)", blank=True, null=True
    )
    true_answer = models.CharField(
        max_length=10,
        choices=[("а", "А"), ("б", "Б"), ("в", "В"), ("г", "Г"), ("д", "Д")],
        verbose_name="Правильный ответ",
    )
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def save(self, *args, **kwargs):
        if self.question_number is None:
            last_question = (
                TestContent.objects.filter(test=self.test)
                .order_by("question_number")
                .last()
            )
            self.question_number = (
                (last_question.question_number + 1) if last_question else 1
            )
        super().save(*args, **kwargs)

    def clean(self):
        if self.var_A_image and self.var_A_text:
            raise ValidationError(
                {
                    "var_A_image": "Выберите только один вариант для A: либо текст, либо файл",
                    "var_A_text": "Выберите только один вариант для A: либо текст, либо файл",
                }
            )
            
        if self.var_B_image and self.var_B_text:
            raise ValidationError(
                {
                    "var_B_image": "Выберите только один вариант для B: либо текст, либо файл",
                    "var_B_text": "Выберите только один вариант для B: либо текст, либо файл",
                }
            )
            
        if self.var_C_image and self.var_C_text:
            raise ValidationError(
                {
                    "var_C_image": "Выберите только один вариант для C: либо текст, либо файл",
                    "var_C_text": "Выберите только один вариант для C: либо текст, либо файл",
                }
            )
            
        if self.var_D_image and self.var_D_text:
            raise ValidationError(
                {
                    "var_D_image": "Выберите только один вариант для D: либо текст, либо файл",
                    "var_D_text": "Выберите только один вариант для D: либо текст, либо файл",
                }
            )

        if self.question_text and self.question_image:
            raise ValidationError(
                {
                    "question_image": "Выберите только один вариант для вопроса: либо текст, либо файл",
                    "question_text": "Выберите только один вариант для вопроса: либо текст, либо файл",
                }
            )
        if self.var_E_image and self.var_E_text:
            raise ValidationError(
                {
                    "var_E_image": "Выберите только один вариант для Д: либо текст, либо файл",
                    "var_E_text": "Выберите только один вариант для Д: либо текст, либо файл",
                }
            )

    def __str__(self):
        return f"Вопрос {self.question_number} для {self.test.test_name}"

    class Meta:
        verbose_name = "Вопрос теста"
        verbose_name_plural = "Вопросы тестов"


class TestFullDescription(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    description_title = models.CharField(
        max_length=60, verbose_name="Название описания"
    )
    description_image = models.ImageField(
        upload_to="TestFullDescription/", verbose_name="Описаниев в формате изображения"
    )
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.test.test_name} - {self.description_title}"

    class Meta:
        verbose_name = "Подробное описание теста"
        verbose_name_plural = "Подробные описания тестов"


class TestInstruction(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    instruction_title = models.CharField(
        max_length=60, verbose_name="Название инструкции"
    )
    instruction_image = models.ImageField(
        upload_to="TestInstruction/", verbose_name="Инструкция в формате изображения", blank=True, null=True
    )
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.test.test_name} - {self.instruction_title}"

    class Meta:
        verbose_name = "Инструкция теста"
        verbose_name_plural = "Инструкции тестов"


class MockAssessmentTest(models.Model):
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,13}$", 
        message="Введите корректный номер телефона"
    )
    phone_number = models.CharField(
        validators=[phone_regex], 
        max_length=13, 
        unique=True, 
        verbose_name="Номер телефона",
    )
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    last_update_date = models.DateTimeField(
        auto_now=True, 
        verbose_name="Дата последнего обновления"
    )
    created_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата создания"
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone_number}"

    class Meta:
        verbose_name = "Пробная запись на оценочный тест"
        verbose_name_plural = "Пробные записи на оценочные тесты"


class MockAssessmentAnswer(models.Model):
    mock_test = models.ForeignKey(MockAssessmentTest, on_delete=models.CASCADE, related_name='answers')
    test_content = models.ForeignKey(TestContent, on_delete=models.CASCADE, verbose_name="Тест контент")

    question_number = models.IntegerField()
    answer_vars = models.CharField(
        max_length=1,
        choices=[("а", "А"), ("б", "Б"), ("в", "В"), ("г", "Г"), ("д", "Д")],
        verbose_name="Ответ студента",
    )
    last_update_date = models.DateTimeField(
        auto_now=True, 
        verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата создания"
    )
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ?")

    def __str__(self):
        return f"Ответ {self.mock_test.first_name} на вопрос {self.question_number}"

    class Meta:
        verbose_name = "Ответ на пробный тест"
        verbose_name_plural = "Ответы на пробные тесты"


class UserStatistic(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    user = models.ForeignKey(
        MockAssessmentTest, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    true_answer_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество правильных ответов"
    )
    false_answer_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество неправильных ответов"
    )
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата создания"
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.test.test_name} - правильные: {self.true_answer_count}, неправильные: {self.false_answer_count}"

    class Meta:
        verbose_name = "Статистика ответов"
        verbose_name_plural = "Статистики ответов"
        unique_together = ("test", "user")
