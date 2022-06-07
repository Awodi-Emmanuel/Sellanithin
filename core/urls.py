from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenRefreshView

from .api_views import ProductViewset, CategoryViewset


router = DefaultRouter()
router.register("product", ProductViewset, basename="product")
router.register("category", CategoryViewset, basename="category")




urlpatterns = []

urlpatterns += router.urls
