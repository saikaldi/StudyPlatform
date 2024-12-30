from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class CategoryVideo(models.Model):
    """Моделка для сохранения информации о категориях видео"""
    
    name = models.CharField("Название", max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL", blank=True)
    created_data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.name}')
        super().save(*args, **kwargs)
        
    class Meta:
        db_table = "category_video"
        

class Video(models.Model):
    """"Моделка для сохранения информации о видео"""
    
    subject = models.CharField("Название тема урока", max_length=100)
    description = models.TextField("Описание темы урока")
    category = models.ForeignKey(CategoryVideo, on_delete=models.CASCADE, related_name="videos", blank=True,)
    video_url = models.URLField("Ссылка на видео", max_length=100)
    is_paid = models.BooleanField("Является ли видео платным?", default=False)
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL", blank=True)
    created_data = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'Урок {self.category.name}: {self.subject}'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.subject}")
        super().save(*args, **kwargs)
        
    def get_video_type(self):  # возвращает строку с типом видео
        return "Платное" if self.is_paid else "Бесплатное"
       
    
    class Meta:
        db_table = "video"
    
    
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
    
    text = models.TextField("Текст вопроса")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name="questions")
    id_question = models.IntegerField("Номер вопроса")
    
    """Варианты ответов на вопрос"""
    
    answer_a = models.TextField("Вариянт А",  max_length=255, blank=True, null=True)
    answer_b = models.TextField("Вариянт Б", max_length=255, blank=True, null=True)
    answer_c = models.TextField("Вариянт В", max_length=255, blank=True, null=True)   
    answet_d = models.TextField("Вариянт Г", max_length=255, blank=True, null=True)
    is_correct = models.CharField("Правилный ответ", max_length=1,  choices=IS_CORRECT_CHOICES)
    is_paid = models.BooleanField("Является ли тест платным?", default=False)
    created_data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Вопрос {self.id_question} в уроке {self.video.subject}'  

    
    class Meta:
        db_table = "test"

    
class UserAnswer(models.Model):
    """Моделка для сохранения информации о ответах на вопросы урока"""
    CHOICES = (
        ("A", "A"),
        ("Б", "Б"),
        ("В", "В"),
        ("Г", "Г"),
    )
    
    qiestion = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="user_answers")
    answer = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="user_answers")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_answers")
    answer = models.CharField(verbose_name="Ответ на вопрос", max_length=1, choices=CHOICES)
    created_data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Учитель {self.student.username} ответил на вопрос {self.answer.id_question} в уроке {self.answer.question_video.subject}'
    
    def user_answer(self):
        user_answer = UserAnswer.objects.filter(student=self.student)
        correst_answer = user_answer.count()
        total_question = user_answer.count()
        
        for user_answer in user_answer:
            correst_answer += 1 
        
        return (correst_answer, total_question)
    
    
    class Meta:
        db_table = "user_answer"
    
    
class Result(models.Model):
    """Моделка для сохранения информации о результатах теста"""
    
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="results")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="results")
    result = models.CharField(verbose_name="Результат теста", max_length=255)
    created_data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Результат теста {self.test.id_question} для студента {self.student.username}'
    
    
    class Meta: 
        db_table = "result"
    
