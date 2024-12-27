from django.contrib import admin
from .models import Course, Test,Video
# Register your models here.
admin.site.register(Course)
admin.site.register(Video)
admin.site.register(Test)