from django.contrib import admin
from .models import Product, ProductAccess, Lesson, LessonView

admin.site.register(Product)
admin.site.register(ProductAccess)
admin.site.register(Lesson)
admin.site.register(LessonView)
