from django.db import models
from ..users.models import User
from django.core.exceptions import ValidationError


def upload_to_test(instance, filename):
    if hasattr(instance, "test") and instance.test:
        return f"{instance.test.title}/{filename}"
    return f"unknown/{filename}"

class TestCategory(models.Model):
    test_category_name = models.CharField(
        max_length=52, verbose_name="Название типа теста"
    )
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.test_category_name

    class Meta:
        verbose_name = "Категория предмета"
        verbose_name_plural = "1. Категории предметов"


class SubjectCategory(models.Model):
    subject_category_name = models.CharField(
        max_length=52, verbose_name="Название типа теста"
    )
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.subject_category_name

    class Meta:
        verbose_name = "Категория теста"
        verbose_name_plural = "2. Категории тестов"


class Test(models.Model):
    test_category = models.ForeignKey(
        TestCategory, on_delete=models.CASCADE, verbose_name="Категория теста"
    )
    subject_category = models.ForeignKey(
        SubjectCategory, on_delete=models.CASCADE, verbose_name="Категория предмета"
    )
    title = models.CharField(max_length=100, verbose_name="Название теста")
    first_test = models.BooleanField(
        default=False, verbose_name="Обозначение будет ли тест первым бесплатным тестом"
    )
    description = models.TextField(verbose_name="Описание теста")
    background_image = models.ImageField(
        upload_to="test_background_image/", verbose_name="Фоновое изображение"
    )
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "3. Тесты"


class TestContent(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    question_number = models.PositiveIntegerField(
        verbose_name="Номер вопроса", blank=True, null=True
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
        return f"{self.test.test_category.test_category_name} - {self.test.title} - {self.true_answer}"

    class Meta:
        verbose_name = "Вопрос теста"
        verbose_name_plural = "6. Вопросы тестов"


class TestFullDescription(models.Model):
    test_category = models.ForeignKey(
        TestCategory, on_delete=models.CASCADE, verbose_name="Категория теста"
    )
    description_title = models.CharField(
        max_length=60, verbose_name="Название описания"
    )
    description = models.TextField(verbose_name="Описание")
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.test_category.test_category_name} - {self.description_title}"

    class Meta:
        verbose_name = "Подробное описание теста"
        verbose_name_plural = "4. Подробные описания тестов"


class OkupTushunuu(models.Model):
    """
    Represents a test with a name and description.
    """

    name = models.CharField(
        max_length=255, verbose_name="Название теста", default="Default Title"
    )
    description = models.TextField(verbose_name="Описание теста")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Окуп тушунуу"
        verbose_name_plural = "5. Окуп тушунуу"


class OkupTushunuuText(models.Model):
    """
    Represents a text with a title and file for comprehension.
    """

    test = models.ForeignKey(
        OkupTushunuu,
        on_delete=models.CASCADE,
        related_name="texts",
        verbose_name="Тест",
    )
    question_number = models.PositiveIntegerField(
        verbose_name="Номер текста", blank=True, null=True
    )
    title = models.CharField(
        max_length=255, verbose_name="Название текста", default="Default Title"
    )
    text_file = models.FileField(
        upload_to="okup_tushunuu_files/",
        blank=True,
        null=True,
        verbose_name="Файл текста",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Текст - Окуп тушунуу"
        verbose_name_plural = "7. Тексты - Окуп тушунуу"


class OkupTushunuuQuestion(models.Model):
    """
    Represents a question with multiple-choice answers, correct answer, and user answers.
    """

    question = models.ForeignKey(
        OkupTushunuuText,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Текст",
    )
    question_number = models.PositiveIntegerField(
        verbose_name="Номер вопроса", blank=True, null=True
    )
    question_text = models.TextField(
        verbose_name="Вопрос", default="Default question text"
    )
    var_A_text = models.TextField(
        verbose_name="Вариант ответа 'А'", blank=True, null=True
    )
    var_B_text = models.TextField(
        verbose_name="Вариант ответа 'Б'", blank=True, null=True
    )
    var_C_text = models.TextField(
        verbose_name="Вариант ответа 'В'", blank=True, null=True
    )
    var_D_text = models.TextField(
        verbose_name="Вариант ответа 'Г'", blank=True, null=True
    )
    true_answer = models.CharField(
        max_length=10,
        choices=[("а", "А"), ("б", "Б"), ("в", "В"), ("г", "Г")],
        verbose_name="Правильный ответ",
        default="а",  # Provide a default value
    )

    def __str__(self):
        return f"{self.question_text} (Текст: {self.question.title})"

    class Meta:
        verbose_name = "Вопрос Окуп тушунуу"
        verbose_name_plural = "8. Вопросы Окуп тушунуу"


class UserStatistic(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    okup_tushunuu = models.ForeignKey(
        OkupTushunuu,
        on_delete=models.CASCADE,
        verbose_name="Окуп тушунуу",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
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
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        if self.okup_tushunuu:
            return f"{self.user.email} - {self.okup_tushunuu.name} - правильные: {self.true_answer_count} - неправильные: {self.false_answer_count}"

        return f"{self.user.email} - {self.test.title} - правильные ответы: {self.true_answer_count} - неправильные ответы: {self.false_answer_count}"

    class Meta:
        verbose_name = "Счет ответов"
        verbose_name_plural = "10. Счета ответов"
        unique_together = ("test", "user")


class UserAnswer(models.Model):
    test_content = models.ForeignKey(
        TestContent, on_delete=models.CASCADE, verbose_name="Тест контент"
    )
    okup_tushunuu_question = models.ForeignKey(
        OkupTushunuuQuestion,
        on_delete=models.CASCADE,
        verbose_name="Вопрос Окуп Тушунуу",
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )

    answer_vars = models.CharField(
        max_length=1,
        choices=[("а", "А"), ("б", "Б"), ("в", "В"), ("г", "Г")],
        verbose_name="Ответ студента",
    )
    # output_time = models.PositiveIntegerField(
    #     default=1, verbose_name="Время ответа (в секундах)"
    # )
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        if self.okup_tushunuu_question:
            return f"{self.user.email} - {self.okup_tushunuu_question.question_text} - {self.answer_vars}"
        return f"{self.user.email} - {self.test_content.test.title}"

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "9. Ответы пользователей"
