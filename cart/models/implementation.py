from .abstration import Cart as AbstractCart
from .abstration import DeliveryCost as AbstractDeliveryCost
from .abstration import Campaign as AbstractCampaign
from .abstration import Coupon as AbstractCoupon
from .abstration import Order as AbstractOrder


class Cart(AbstractCart):
    pass

class DeliveryCost(AbstractDeliveryCost):
    pass

class Campaign(AbstractCampaign):
    pass

class Coupon(AbstractCoupon):
    pass

class Order(AbstractOrder):
    pass