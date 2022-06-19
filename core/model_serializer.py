from dataclasses import field
from typing import Union


from django.contrib.auth import get_user_model
from rest_framework.serializers import CharField, IntegerField, ListSerializer
from rest_framework.serializers import ModelSerializer as DrfModelSerializer
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework_simplejwt.tokens import RefreshToken

from core.models.implementation import(
    Category,
    Product,
    Cart,
    DeliveryCost,
    Campaign,
    Coupon,
) 

User = get_user_model()

class MyListSerializer(ListSerializer):
    @property
    def data(self):
        ret = super().data
        return ReturnList(ret, serializer=self)
    
class ModelSerializer(DrfModelSerializer):
    class Meta:
        list_serializer_class = MyListSerializer  
        
        
class PublicUserSerializer(ModelSerializer):
    id = IntegerField()
    username = CharField(required=False) 
    
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "is_active") 
        
class UserSerializer(ModelSerializer):
    id = IntegerField()
    
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "email_is_verified"
        )
        
    def get_tokens(self, instance: User) -> Union[dict, None]:
        refresh = RefreshToken.for_user(instance)
        
            # print('refresh: ' + str(refresh))
            # print('access_token: ' + str(refresh.access_token))
            
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }                 

class CategorySerializer(ModelSerializer):
    id = IntegerField()
    
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "parent_category_id",
            "slug",
            "created_at",
            "updated_at"
        )   

class ProductSerializer(ModelSerializer):
    id = IntegerField()
    
    class Meta:
        model =  Product
        fields = (
            "id",
            "category",
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "available",
            "created_at",
            "updated"
        )
        
        
class CartSerailizer(ModelSerializer):
    id = IntegerField()
    
    class Meta:
        model = Cart
        fields = (
            "id",
            "user",
            "item",
            "quantity",
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
    id = IntegerField()
    
    class Meta:
        model = Coupon
        fields = ("minimum_cart_amount", "discount_rate", "created_at", "updated_at")             
        
        