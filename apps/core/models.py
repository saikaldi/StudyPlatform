
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Create your models here.


class Graduate(models.Model):
    name = models.CharField("Имя", max_length=25)
    lastname = models.CharField("Фамилия", max_length=25)
    image = models.ImageField("Фотография", upload_to="graduates/images")
    grade = models.IntegerField('Оценка', default=0)
    review = models.TextField("Отзыв")
    created_data = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name + " " + self.lastname
    
    

class AbountUs(models.Model):   
    title = models.CharField('Заголовок', max_length=25)
    text = models.TextField('О нас')
    image = models.ImageField('Фотография', upload_to='aboutus/images')
    our_team = models.TextField('Кратко о нашей команде')
    mission = models.TextField('Что мы приложим')
    our_goals = models.TextField('Что мы хотим достичь')
    
    def __str__(self):
        return self.title
    
    
    
class Feedback(models.Model):
    name = models.CharField("Имя", max_length=25)
    lastname = models.CharField("Фамилия", max_length=25)
    gmail = models.EmailField("Gmail", max_length=100)
    phone_number_validator = RegexValidator(regex=r'^(0\d{9}|\+996\d{9})$',
                                            message='Введите правильный номер телефона'
                                            )   
    
    phone_number = models.CharField("Номер телефона", max_length=55, validators=[phone_number_validator])
    
    
    def __str__(self):
        return self.name + " " + self.lastname
    
    
    
    
