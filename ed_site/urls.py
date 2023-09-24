from django.urls import path
from .views import (
    LessonListByProduct,
    LessonListBySpecificProduct,
    ProductStatistics,
    LessonViewCreate,
)

urlpatterns = [
    path("lessons/", LessonListByProduct.as_view(), name="lesson-list-by-product"),
    path(
        "lessons/product/<int:product_id>/",
        LessonListBySpecificProduct.as_view(),
        name="lesson-list-by-specific-product",
    ),
    path("product-statistics/", ProductStatistics.as_view(), name="product-statistics"),
    path("lesson-view/", LessonViewCreate.as_view(), name="lesson-view-create"),
]
