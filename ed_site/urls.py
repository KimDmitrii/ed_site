from django.urls import path
from .views import LessonListByProduct, LessonListBySpecificProduct

urlpatterns = [
    path('lessons/', LessonListByProduct.as_view(), name = 'lesson-list-by-product'),
    path('lessons/product/<int:product_id>/', LessonListBySpecificProduct.as_view(), name = 'lesson-list-by-specific-product'),
]