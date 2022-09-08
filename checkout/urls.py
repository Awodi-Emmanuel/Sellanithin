from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
# from rest_framework_simplejwt.views import TokenVerifyView
# from utils.payment import process_payment
from checkout.api_views import(
    CheckoutViewset,
    PaymentViewset
    
) 


router = DefaultRouter()
router.register("checkout", CheckoutViewset, basename="checkout")
router.register("paywithcard", PaymentViewset, basename="paywithcard")




urlpatterns = []

urlpatterns += router.urls