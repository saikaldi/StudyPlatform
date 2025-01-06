from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from slugify import slugify
from django.core.exceptions import ValidationError

# Create your models here.

class CategoryVideo(models.Model):
    """Моделка для сохранения информации о категориях видео"""
    
    name = models.CharField("Название", max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="children", blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL", blank=True)
    created_data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):  
        if self.parent:
            return f"{self.parent.name}/{self.name}"
        else:   
            return self.name
        
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":  
            base_slug = slugify(f"{self.name}")
            unique_slug = base_slug
            counter = 1
            while CategoryVideo.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"                  
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs) 
    class Meta:
        db_table = "category_video"
        
    class Meta:
        verbose_name = "Категория видео"
        verbose_name_plural = "Категории видео"
        


class Video(models.Model):
    """"Моделка для сохранения информации о видео"""
    
    subject = models.CharField("Название тема урока", max_length=100)
    description = models.TextField("Описание темы урока")
    category = models.ForeignKey(CategoryVideo, on_delete=models.CASCADE, related_name="videos",  verbose_name="Категория видео", blank=True,)
    video_url = models.URLField("Ссылка на видео", max_length=100)
    is_paid = models.BooleanField("Является ли видео платным?", default=False)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL", blank=True)
    created_data = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'Предмет: {self.category.name} Тема:{self.subject}'
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":  
            base_slug = slugify(f"{self.subject}")
            unique_slug = base_slug
            counter = 1
            while Video.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"                  
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs) 
        if self.is_paid:
            self.questions.update(is_paid=True)
        
    def get_video_type(self):  # возвращает строку с типом видео
        return "Платное" if self.is_paid else "Бесплатное"
       
    
    def get_total_questions(self):
        return self.questions.count()


    def get_correct_answers(self, user):
        correct_answers = 0
        for question in self.questions.all():
            user_answer = question.user_answers.filter(student=user).first()
            if user_answer and user_answer.is_correct:
                correct_answers += 1
        return correct_answers
    

    def is_passed(self, user):
        total_questions = self.get_total_questions()
        if total_questions == 0:
            return False
        correct_answers = self.get_correct_answers(user)
        result = (correct_answers / total_questions) * 100
        if result >= 80:
            return True
        
        return False
        
    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"
    
    
#######################################################
""""Вопросы для моделей видео """

class Test(models.Model):
    """Моделка для сохранения информации о вопросах урока"""
    
    IS_CORRECT_CHOICES = (
        ("A", "A"),
        ("Б", "Б"),
        ("В", "В"),
        ("Г", "Г"),
    )
    
    text = models.TextField("Текст вопроса", blank=True, null=True)
    image = models.ImageField("Изображение вопроса", upload_to="question_images/", null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="questions", verbose_name="Видео")    
    image_a = models.ImageField("Изображение варианта А", upload_to="question_images/", null=True, blank=True)
    answer_a = models.TextField("Вариянт А",  max_length=255, blank=True, null=True)
    image_b = models.ImageField("Изображение варианта Б", upload_to="question_images/", null=True, blank=True)
    answer_b = models.TextField("Вариянт Б", max_length=255, blank=True, null=True)
    image_c = models.ImageField("Изображение варианта В", upload_to="question_images/", null=True, blank=True)
    answer_c = models.TextField("Вариянт В", max_length=255, blank=True, null=True)   
    image_d = models.ImageField("Изображение варианта Г", upload_to="question_images/", null=True, blank=True)
    answer_d = models.TextField("Вариянт Г", max_length=255, blank=True, null=True)
    is_correct = models.CharField("Правилный ответ", max_length=1,  choices=IS_CORRECT_CHOICES)
    is_paid = models.BooleanField("Является ли тест платным?")
    created_data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f' Вопрос:{self.text} в уроке {self.video.subject}'
    
    def clean(self):
        if self.text and self.image:
            raise ValidationError("Можно запонить текст или изображение, но не оба")
        
        options = [
            (self.answer_a, self.image_a),
            (self.answer_b, self.image_b),
            (self.answer_c, self.image_c),
            (self.answer_d, self.image_d),
        ]
        
        for text, image in options:
            if not text and not image:
                raise ValidationError("Все варианты должны быть заполнены")
        if text and image:
            raise ValidationError("Можно запонить текст или изображение, но не оба")

    def save(self, *args, **kwargs):
        self.clean()
        if self.video.is_paid:
            self.is_paid = True
        super().save(*args, **kwargs)
        
    
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['-video']
    

class UserAnswer(models.Model):
    """Моделка для сохранения информации о ответах на вопросы урока"""
    
    CHOICES = (
        ("A", "A"),
        ("Б", "Б"),
        ("В", "В"),
        ("Г", "Г"),
    )
    
    question = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="user_answers")
    answer = models.CharField(verbose_name="Ответ на вопрос", max_length=1, choices=CHOICES)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_answers")
    created_data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Студент {self.student} ответил на вопрос {self.answer} в вопросе {self.question}'
    
    def is_correct(self):
        """"Метод для проверки правильности ответа на вопрос"""
        return self.answer == self.question.is_correct
    
    
    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
        ordering = ['-student', '-created_data']
    
    
class Result(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='results')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='results')
    total_questions = models.IntegerField(verbose_name="Всего вопросов", default=0)
    correct_answers = models.IntegerField(verbose_name="Всего правильных ответов", default=0)
    incorrect_answers = models.IntegerField(verbose_name="Всего неправильных ответов", default=0)
    result_percentage = models.FloatField(verbose_name="Результат теста", default=0)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL", blank=True)
    created_data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):  
        return f"{self.student} - {self.video.subject} - {self.result_percentage}%"

    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":  
            base_slug = slugify(f"{self.student}-{self.video.slug}")
            unique_slug = base_slug
            counter = 1
            while Result.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"                  
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"
        ordering = ['-created_data']