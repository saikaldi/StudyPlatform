from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from slugify import slugify


class Subject(models.Model):
    name = models.CharField(max_length=40, verbose_name="Название предмета")
    # slug = models.SlugField(
    #     max_length=255, unique=True, db_index=True, verbose_name="URL"
    # )
    last_updated = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     if not self.slug or self.slug.strip() == "":
    #         base_slug = slugify(self.name, allow_unicode=False)
    #         unique_slug = base_slug
    #         counter = 1
    #         while Subject.objects.filter(slug=unique_slug).exists():
    #             unique_slug = f"{base_slug}-{counter}"
    #             counter += 1
    #         self.slug = unique_slug
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"
        ordering = ["-created_at"]


class Graduate(models.Model):
    first_name = models.CharField("Имя", max_length=25)
    last_name = models.CharField("Фамилия", max_length=25)
    image = models.ImageField("Фотография", upload_to="graduates/images")
    score = models.IntegerField(
        "Баллы", validators=[MinValueValidator(10), MaxValueValidator(245)]
    )
    review = models.TextField("Отзыв")
    # slug = models.SlugField(
    #     max_length=255, unique=True, db_index=True, verbose_name="slug"
    # )
    last_updated = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # def save(self, *args, **kwargs):
    #     if not self.slug or self.slug.strip() == "":
    #         base_slug = slugify(f"{self.first_name} {self.last_name}")
    #         unique_slug = base_slug
    #         counter = 1
    #         while Graduate.objects.filter(slug=unique_slug).exists():
    #             unique_slug = f"{base_slug}-{counter}"
    #             counter += 1
    #         self.slug = unique_slug
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Выпускник"
        verbose_name_plural = "Выпускники"
        ordering = ["-created_at"]


class Teacher(models.Model):
    first_name = models.CharField("Имя", max_length=55)
    last_name = models.CharField("Фамилия", max_length=55)
    subject = models.ForeignKey(
        Subject, verbose_name="Предмет", on_delete=models.CASCADE
    )
    image = models.ImageField("Фотография", upload_to="teachers/images")
    # slug = models.SlugField(
    #     max_length=255, unique=True, db_index=True, verbose_name="slug"
    # )
    last_updated = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # def save(self, *args, **kwargs):
    #     if not self.slug or self.slug.strip() == "":
    #         base_slug = slugify(f"{self.first_name} {self.last_name}")
    #         unique_slug = base_slug
    #         counter = 1
    #         while Teacher.objects.filter(slug=unique_slug).exists():
    #             unique_slug = f"{base_slug}-{counter}"
    #             counter += 1
    #         self.slug = unique_slug
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ["-created_at"]


class Feedback(models.Model):
    first_name = models.CharField("Имя", max_length=25)
    last_name = models.CharField("Фамилия", max_length=25)
    email = models.EmailField("Email", max_length=100)
    phone_number = models.CharField(
        "Номер телефона",
        max_length=55,
        validators=[
            RegexValidator(
                regex=r"^(0\d{9}|\+996\d{9})$",
                message="Введите правильный номер телефона",
            )
        ],
    )
    text = models.TextField("Текст отзыва")
    # slug = models.SlugField(
    #     max_length=255, unique=True, db_index=True, verbose_name="slug"
    # )
    last_updated = models.DateTimeField(
        auto_now=True, verbose_name="Последнее обновление"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    # def save(self, *args, **kwargs):
    #     if not self.slug or self.slug.strip() == "":
    #         base_slug = slugify(
    #             f"{self.first_name} {self.last_name}", allow_unicode=False
    #         )
    #         unique_slug = base_slug
    #         counter = 1
    #         while Feedback.objects.filter(slug=unique_slug).exists():
    #             unique_slug = f"{base_slug}-{counter}"
    #             counter += 1
    #         self.slug = unique_slug
    #     super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]
