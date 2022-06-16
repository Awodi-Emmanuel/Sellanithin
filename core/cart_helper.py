from .models import Cart, DeliveryCost
from .discounts_helper import (
    CampaignHelper,
    CouponHelper
)

class DeliveryCostHelper:
    
    def __init__(self, cart_items):
        self.cart_items = cart_items
        self.calculator = False