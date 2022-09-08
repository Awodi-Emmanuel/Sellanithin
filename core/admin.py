from django.contrib import admin
# from .models.abstration import Users as AdminUSer
# from.models.abstration import TempCode as AdminTempcode
# from .models.abstration import Category as AdminCategory
# from .models.abstration import Product as AdminProduct
# from .models.abstration import Cart as AdminCart
# from .models.abstration import DeliveryCost as AdminDeliverycost
# from .models.abstration import Campaign as AdminCampaign
# from .models.abstration import Coupon as AdminCoupon

from core.models.implementation import (
    Users,
    TempCode,
    # Product,
    # Category,
    # Cart,
    # DeliveryCost,
    # Campaign,
    # Coupon
)

# Register your models here.


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    pass

@admin.register(TempCode)
class TempCodeAdmin(admin.ModelAdmin):
    pass

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     pass

# @admin.register(DeliveryCost)
# class DeliverycostAmin(admin.ModelAdmin):
#     pass

# @admin.register(Campaign)
# class CampaignAdmin(admin.ModelAdmin):
#     pass

# @admin.register(Coupon)
# class CouponAdmin(admin.ModelAdmin):
#     pass