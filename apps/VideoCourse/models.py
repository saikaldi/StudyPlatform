from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from slugify import slugify
from django.core.exceptions import ValidationError


def upload_to_test(instance, filename):
    if hasattr(instance, "video") and instance.video:
        return f"{instance.video.subject_name}/{filename}"
    return f"unknown/{filename}"

class Category(models.Model):
    category_name = models.CharField(max_length=100, verbose_name="Название предмета")
    slug = models.SlugField(
        max_length=100, unique=True, db_index=True, verbose_name="slug", blank=True
    )
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            base_slug = slugify(self.category_name)
            unique_slug = base_slug
            counter = 1
            while CategoryVideo.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Название предмета"
        verbose_name_plural = "1. Название предмета"


class CategoryVideo(models.Model):
    category_name = models.CharField(max_length=100, verbose_name="Название категории")

    slug = models.SlugField(
        max_length=100, unique=True, db_index=True, verbose_name="slug", blank=True
    )
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.category_name

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            base_slug = slugify(self.category_name)
            unique_slug = base_slug
            counter = 1
            while CategoryVideo.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория видео"
        verbose_name_plural = "2. Категории видео"


class SubjectCategory(models.Model):
    subject_category_name = models.CharField(
        max_length=52, verbose_name="Название типа видео"
    )
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.subject_category_name

    class Meta:
        verbose_name = "Под категория видео"
        verbose_name_plural = "3. Под категории видео"


class Video(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="category",
        verbose_name="Категория предмета",
        blank=True,
        null=True,
    )
    video_category = models.ForeignKey(
        CategoryVideo,
        on_delete=models.CASCADE,
        related_name="videos",
        verbose_name="Под категория предмета",
        blank=True,
        null=True,
    )
    subject_category = models.ForeignKey(
        SubjectCategory, on_delete=models.CASCADE, verbose_name=" Предмета"
    )
    subject_name = models.CharField(max_length=100, verbose_name="Название тема урока")
    description = models.TextField(verbose_name="Описание темы урока")
    video_url = models.TextField(verbose_name="Ссылка на видео")
    video_order = models.PositiveIntegerField(verbose_name="Порядковый номер")
    is_paid = models.BooleanField(
        default=False, verbose_name="Является ли видео платным?"
    )
    slug = models.SlugField(
        max_length=100, unique=True, db_index=True, verbose_name="slug", blank=True
    )
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Предмет: {self.video_category.category_name} Тема:{self.subject_name}"

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            base_slug = slugify(f"{self.subject_name}")
            unique_slug = base_slug
            counter = 1
            while Video.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "4. Видео"
        ordering = ["video_order"]


class TestContent(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="Тест")
    question_text = models.TextField(verbose_name="Вопрос в текстовом формате")
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
    test_order = models.PositiveIntegerField(
        unique=True, verbose_name="Порядковый номер"
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
        return f"{self.video.video_category.category_name} - {self.video.subject_name} - {self.true_answer}"

    class Meta:
        verbose_name = "Вопрос теста"
        verbose_name_plural = "5. Вопросы тестов"
        ordering = ["test_order"]
        unique_together = ("video", "test_order")


class UserStatistic(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, verbose_name="Тест")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="user_statistics_videocourse",
    )
    true_answer_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество правильных ответов"
    )
    false_answer_count = models.PositiveIntegerField(
        default=0, verbose_name="Количество неправильных ответов"
    )
    accuracy_percentage = models.FloatField(
        default=0.0, verbose_name="Процент правильных ответов"
    )
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def update_accuracy(self):
        total_answers = self.true_answer_count + self.false_answer_count
        if total_answers > 0:
            self.accuracy_percentage = (self.true_answer_count / total_answers) * 100
        else:
            self.accuracy_percentage = 0.0
        self.save()

    def __str__(self):
        return f"{self.user.email} - {self.video.subject_name} - правильные ответы: {self.true_answer_count} - неправильные ответы: {self.false_answer_count} - точность: {self.accuracy_percentage}%"

    class Meta:
        verbose_name = "Счет ответов"
        verbose_name_plural = "6. Счета ответов"
        unique_together = ("video", "user")


class UserAnswer(models.Model):
    test_content = models.ForeignKey(
        TestContent, on_delete=models.CASCADE, verbose_name="Тест контент"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="user_answer_videocourse",
    )
    answer_vars = models.CharField(
        max_length=1,
        choices=[("a", "A"), ("b", "B"), ("c", "C"), ("d", "D")],
        verbose_name="Ответ",
    )
    output_time = models.PositiveIntegerField(
        default=1, verbose_name="Время ответа (в секундах)"
    )
    last_update_date = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.user.email} - {self.test_content.video.subject_name}"

    class Meta:
        verbose_name = "Ответ пользователя"
        verbose_name_plural = "7. Ответы пользователей"
