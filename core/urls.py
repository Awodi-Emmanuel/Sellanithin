from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
# from rest_framework_simplejwt.views import TokenVerifyView
from utils.payment import process_payment
from core.api_views import(
    AuthViewset,
    # AdminProductViewset,
    # CustomerProductViewset, 
    # AdminCategoryViewset,
    # CustomerCategoryViewset,
    # CartViewset,
    # CampaignViewset,
    # CouponViewset,
    # PaymentViewset
) 


router = DefaultRouter()
router.register("auth", AuthViewset, basename="auth")
# router.register("product", CustomerProductViewset, basename="product")
# router.register("admin/product", AdminProductViewset, basename="admin/product")

# router.register("category", CustomerCategoryViewset, basename="category")
# router.register("admin/category", AdminCategoryViewset, basename="admin/category")

# router.register("cart", CartViewset, basename="cart")
# router.register("discounts/campaign", CampaignViewset, basename="campaign")
# router.register("discounts/coupon", CouponViewset, basename="coupon")

# router.register("payment", PaymentViewset, basename="payment")
# router.register("callback", process_payment, basename="callback")



urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("callback", process_payment, name="callback")
]

urlpatterns += router.urls