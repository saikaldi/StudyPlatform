from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Subject(models.Model):
    name = models.CharField(max_length=100)  # Название предмета

class Lesson(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(max_length=200)  # Название урока
    video_url = models.URLField()  # Ссылка на видео урок
    order = models.PositiveIntegerField()  # Порядок уроков в предмете

class Question(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()  # Текст вопроса
    option_a = models.CharField(max_length=200)  # Вариант А
    option_b = models.CharField(max_length=200)  # Вариант Б
    option_c = models.CharField(max_length=200)  # Вариант В
    option_d = models.CharField(max_length=200)  # Вариант Г
    correct_option = models.CharField(max_length=1, 
                    choices=(('A', 'A'), ('Б', 'Б'), ('В', 'В'), ('Г', 'Г'))
                                      )  # Правильный вариант (A, B, C, D)

class UserLessonProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="lesson_progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)  # Результат теста
    attempts = models.PositiveIntegerField(default=0)  # Количество попыток