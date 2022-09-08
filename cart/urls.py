
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cart.api_views import (
    CartViewset,
    CampaignViewset,
    CouponViewset,
    # PaymentViewset
)

router = DefaultRouter()
router.register("cart", CartViewset, basename="cart")
router.register("discounts/campaign", CampaignViewset, basename="campaign")
router.register("discounts/coupon", CouponViewset, basename="coupon")

# router.register("payment", PaymentViewset, basename="payment")
# router.register("callback", process_payment, basename="callback")

urlpatterns = []

urlpatterns += router.urls