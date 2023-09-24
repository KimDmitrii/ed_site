from django.shortcuts import render
from rest_framework import generics
from .models import Product, Lesson, ProductAccess, LessonView
from rest_framework.response import Response
from django.db.models import Count, Sum
from .serializers import (
    LessonSerializer,
    ProductStatisticsSerializer,
    LessonViewSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


# Список всех уроков
class LessonListByProduct(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        accessible_products = ProductAccess.objects.filter(user=user).values_list(
            "product", flat=True
        )
        return Lesson.objects.filter(products__in=accessible_products)


# Список уроков по конкретному продукту с доступом
class LessonListBySpecificProduct(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        product_id = self.kwargs["product_id"]  # Получаем идентификатор продукта из URL
        # Проверяем, имеет ли пользователь доступ к этому продукту
        if not ProductAccess.objects.filter(user=user, product_id=product_id).exists():
            return Lesson.objects.none()  # Если доступа нет, возвращаем пустой queryset
        return Lesson.objects.filter(product=product_id)


# Представление для запросов для получения статистики
class ProductStatistics(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductStatisticsSerializer

    def get_queryset(self):
        user = self.request.user
        # Статистика по продуктам
        queryset = Product.objects.annotate(
            lesson_count=Count("lessons", distinct=True),
            user_count=Count("productaccess__user", distinct=True),
            total_wathc_time=Sum("lessons__lessonview__watch_time_sec", distinct=True),
        ).filter(productaccess__user=user)

        # Конверсия
        for product in queryset:
            product.access_count = ProductAccess.objects.filter(product=product).count()
            if product.access_count > 0:
                product.purchase_percentage = (
                    product.access_count / product.user_count
                ) * 100
            else:
                product.purchase_percentage = 0.0

        return queryset


class LessonViewCreate(generics.CreateAPIView):
    serializer_class = LessonViewSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_id = serializer.validated_data["user"]
        lesson_id = serializer.validated_data["lesson"]
        watch_time_sec = serializer.validated_data["watch_time_sec"]

        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            return Response(
                {"detail": "Урок не найден"}, status=status.HTTP_404_NOT_FOUND
            )

        if watch_time_sec >= (lesson.duration_seconds * 0.8):
            watched = True
        else:
            wathced = False

        LessonView.objects.create(
            user_id=user_id,
            lesson=lesson,
            watched=watched,
            watch_time_sec=watch_time_sec,
        )

        return Response(
            {"detail": "Просмотр урока зарегистрирован"}, status=status.HTTP_201_CREATED
        )
