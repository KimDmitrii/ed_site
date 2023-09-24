from django.shortcuts import render
from rest_framework import generics
from .models import Product, Lesson, ProductAccess, LessonView
from rest_framework.response import Response
from django.db.models import Count, Sum
from .serializers import LessonSerializer
from rest_framework.permissions import IsAuthenticated

# Список всех уроков
class LessonListByProduct(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accessible_products = ProductAccess.objects.filter(user = user).values_list('product', flat=True)
        return Lesson.objects.filter(products__in = accessible_products)
    
# Список уроков по конкретному продукту с доступом
class LessonListBySpecificProduct(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs['product_id'] # Получаем идентификатор продукта из URL
        # Проверяем, имеет ли пользователь доступ к этому продукту
        if not ProductAccess.objects.filter(user=user, product_id = product_id).exists():
            return Lesson.objects.none() # Если доступа нет, возвращаем пустой queryset
        return Lesson.objects.filter(product = product_id)
    
# Представление для запросов для получения статистики
class ProductStatistics(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = self.request.user
        # Статистика по продуктам
        product_stats = Product.objects.annotate(
            lesson_count = Count('lessons', distinct=True),
            user_count = Count('productaccess__user', distinct=True),
            total_wathc_time = Sum('lessons__lessonview__watch_time_sec', distinct=True)
        ).filter(productaccess__user=user)

    # Конверсия, %
    for product in product_stats:
        product.access_count = ProductAccess.objects.filter(product=product).count()
        