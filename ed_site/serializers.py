from rest_framework import serializers
from .models import Product, ProductAccess, Lesson, LessonView


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class ProductAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAccess
        fields = "__all__"


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class LessonViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonView
        fields = "__all__"


class ProductStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "lesson_count",
            "user_count",
            "total_watch_time",
            "access_count",
            "purchase_percentage",
        )


class LessonViewSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    lesson = serializers.IntegerField()
    watch_time_sec = serializers.IntegerField()
