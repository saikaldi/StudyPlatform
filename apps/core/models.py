from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from slugify import slugify





# Create your models here.


class Graduate(models.Model):
    
    """Моделка для сохранения информации о выпускниках"""
    
    name = models.CharField("Имя", max_length=25)
    lastname = models.CharField("Фамилия", max_length=25)
    image = models.ImageField("Фотография", upload_to="graduates/images")
    score = models.IntegerField("Баллы",validators=[MinValueValidator(10), MaxValueValidator(245)])
    review = models.TextField("Отзыв")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    created_data = models.DateTimeField(auto_now_add=True)
       
    def __str__(self):
        return self.name + " " + self.lastname
    
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":  
            base_slug = slugify(f"{self.name} {self.lastname}")    
            unique_slug = base_slug
            counter = 1
            while Graduate.objects.filter(slug=unique_slug).exists():  
                unique_slug = f"{base_slug}-{counter}"                  
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs) 
        

        
    class Meta:
        verbose_name = "Выпускник"
        verbose_name_plural = "Выпускники"
        ordering = ['-created_data']
    

class AbountTeacher(models.Model):
    '''Моделка для сохранения информации о преподавателях'''
    
    CHOICES_TEACHER_TYPE = (
        ('математика', 'математика'),
        ('кыргыз ', 'кыргыз тил'),
        ('физика', 'физика'),
        ('химия', 'химия'),
        ('биология', 'биология'),
        ('тарых', 'тарых'),
    )
    
    name = models.CharField("Имя", max_length=55) 
    lastname = models.CharField("Фамилия", max_length=55)
    teacher_type = models.CharField("Тип преподавателя", max_length=55, choices=CHOICES_TEACHER_TYPE)
    image = models.ImageField("Фотография", upload_to="teachers/images")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    created_data = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name + " " + self.lastname
    
    
    def save(self, *args, **kwargs): 
        if not self.slug or self.slug.strip() == "":  
            base_slug = slugify(f"{self.name} {self.lastname}")  # Аты, фамилия жана teacher_type'дан slug түзүү
            unique_slug = base_slug
            counter = 1
            while AbountTeacher.objects.filter(slug=unique_slug).exists():  # Уникалдуулукту текшерүү
                unique_slug = f"{base_slug}-{counter}"  # Уникалдуу slug түзүү
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)  #
        
    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ['-created_data']
    
    
    
class Feedback(models.Model):
    """Моделка для сохранения информации о отзывах пользователей"""
    
    name = models.CharField("Имя", max_length=25)
    lastname = models.CharField("Фамилия", max_length=25)
    gmail = models.EmailField("Gmail", max_length=100)
    phone_number_validator = RegexValidator(regex=r'^(0\d{9}|\+996\d{9})$',
                                            message='Введите правильный номер телефона'
                                            )   
    phone_number = models.CharField("Номер телефона", max_length=55, validators=[phone_number_validator])
    text = models.TextField("Текст отзыва")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    created_data = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name + " " + self.lastname
    
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":  
            base_slug = slugify(f"{self.name} {self.lastname}", allow_unicode=False)
            unique_slug = base_slug
            counter = 1
            while Feedback.objects.filter(slug=unique_slug).exists():  
                unique_slug = f"{base_slug}-{counter}"  
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs) 
        
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ['-created_data']
    
    
    
    
