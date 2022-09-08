from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api_views import (
    AdminProductViewset,
    CustomerProductViewset, 
    AdminCategoryViewset,
    CustomerCategoryViewset,
)

router = DefaultRouter()
router.register("product", CustomerProductViewset, basename="product")
router.register("admin/product", AdminProductViewset, basename="admin/product")

router.register("category", CustomerCategoryViewset, basename="category")
router.register("admin/category", AdminCategoryViewset, basename="admin/category")


urlpatterns = []

urlpatterns += router.urls