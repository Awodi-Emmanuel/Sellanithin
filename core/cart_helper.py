from .models import Cart, DeliveryCost
from .discounts_helper import (
    CampaignHelper,
    CouponHelper
)

from .responses import(
    CreatedResponse,
    GoodResponse,
    BadRequestResponse,
    NotFoundResponse  
)

class DeliveryCostHelper:
    
    def __init__(self, cart_items):
        self.cart_items = cart_items
        self.calculator = False
        self.number_of_deliveries = 0
        self.number_of_products = 0
        self.cost = 0
        
    def calculate_delivery_cost(self):
        try:
            self.calculator = DeliveryCost.objects.get(status="Active")
            
            delivery_categories = []
            
            for cart_item in self.cart_items:
                self.number_of_products += 1
                if cart_item.item.category.id not in delivery_categories:
                    delivery_categories.append(cart_item.item.category.id)
                    self.number_of_deliveries += 1
                    
                self.cost = (self.calculator.cost_per_delivery * self.number_of_deliveries) + \
                            (self.calculator.cost_per_product * self.number_of_products) + self.calculator.fixed_cost
            return self.cost                   
                    
        except Exception as e:
            return BadRequestResponse(str(e), "Unknown", request=self.request)   