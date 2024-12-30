from django.contrib import admin

from .models import CategoryVideo, Video, Test, UserAnswer

# Register your models here.

class CategoryVideoAdmin(admin.ModelAdmin):
    """Администратор для модели CategoryVideo"""
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    

class VideoAdmin(admin.ModelAdmin):
    """Администратор для модели Video"""
    list_display = ("subject", "category", "get_video_type")
    prepopulated_fields = {"slug": ("subject",)}
    
    def get_video_type(self, obj):
        return obj.get_video_type()


admin.site.register(CategoryVideo, CategoryVideoAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(UserAnswer)
admin.site.register(Test)