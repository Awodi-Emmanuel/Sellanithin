from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenRefreshView

from .api_views import ProductViewset


router = DefaultRouter()
router.register("product", ProductViewset, basename="product")


urlpatterns = []

urlpatterns += router.urls
