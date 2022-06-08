from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
# from rest_framework_simplejwt.views import TokenVerifyView

from core.api_views import(
    AuthViewset,
    ProductViewset, 
    CategoryViewset,
) 


router = DefaultRouter()
router.register("auth", AuthViewset, basename="auth")
router.register("product", ProductViewset, basename="product")
router.register("category", CategoryViewset, basename="category")




urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
