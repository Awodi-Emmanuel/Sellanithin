from dataclasses import field
from django.contrib.auth import get_user_model
from rest_framework.serializers import CharField, IntegerField, ListSerializer
from rest_framework.serializers import ModelSerializer as DrfModelSerializer
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework_simplejwt.tokens import RefreshToken



from cart.models.implementation import(
    Order,
    Cart,
    DeliveryCost,
    Campaign,
    Coupon,
) 


class MyListSerializer(ListSerializer):
    @property
    def data(self):
        ret = super().data
        return ReturnList(ret, serializer=self)
    
class ModelSerializer(DrfModelSerializer):
    class Meta:
        list_serializer_class = MyListSerializer  
        
        
class CartSerailizer(ModelSerializer):
    id = IntegerField()
    
    class Meta:
        model = Cart
        fields = (
            "id",
            "user",
            "item",
            "quantity",
            "purchased",
            "created_at",
            "updated_at"
        )  
        
        
class DeliveryCostSerializer(ModelSerializer):
    id = IntegerField()
    
    class Meta:
        model = DeliveryCost
        fields = ("status", "cost_per_delivery", "cost_per_product", "fixed_cost", "created_at", "updated_at")
                          
        
class  CampaignSerializer(ModelSerializer):
    id = IntegerField()
    
    class Meta:
        model = Campaign
        fields = (
            "id",
            "discount_type",
            "discount_rate",
            "discount_amount",
            "min_purchased_items",
            "apply_to",
            "target_product",
            "target_category",
            "created_at",
            "updated_at"
        )   
        
        
class CouponSerializer(ModelSerializer):
    # id = IntegerField()
    
    class Meta:
        model = Coupon
        fields = ("id", "minimum_cart_amount", "discount_rate", "created_at", "updated_at")
        
        
        
class OrderSerializer(ModelSerializer):
    id = IntegerField()
    
    class Meta:
        model = Order
        field = (
            "orderitems",
            "user",
            "ordered",
            "created",
            "orderId"
        )             
        
        