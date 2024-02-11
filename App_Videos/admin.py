from django.contrib import admin
from .models import Category, Video, Comment, Feedback

admin.site.register(Category)
admin.site.register(Video)
admin.site.register(Comment)
admin.site.register(Feedback)