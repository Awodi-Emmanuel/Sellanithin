
from rest_framework.decorators import action
from django.db.models import Q
from drf_yasg import openapi  # type: ignore
from drf_yasg.utils import swagger_auto_schema


from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
)

from core.custom_classes import YkGenericViewSet
from core.cart_helper import CartHelper, DeliveryCostHelper
from cart.model_serializer import(
    CampaignSerializer,
    CouponSerializer,
    OrderSerializer,
    CartSerailizer
)
from cart.models.implementation import Cart, Order, Coupon, Campaign, DeliveryCost
from core.responses_serialisers import (
    EmptySerializer,
    NotFoundResponseSerializer,
    BadRequestResponseSerializer,
    
)
from core.responses import(
    CreatedResponse,
    GoodResponse,
    BadRequestResponse,
    NotFoundResponse  
)

from django.contrib.auth import get_user_model
User = get_user_model()

class  CartViewset(
    YkGenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,):
    queryset = Cart.objects.all().order_by('id')
    serializer_class = CartSerailizer
    
    @swagger_auto_schema(
        operation_summary="Cart",
        operation_description="Add to card",
        responses={
            200: EmptySerializer(),
            400: BadRequestResponseSerializer(),
        },
    )
    @action(methods=["GET"], detail= False, url_path='checkout/(?P<userId>[^/.]+)', url_name='checkout')
    def checkout(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=int(kwargs.get('userId'))) 
            cart_helper = CartHelper(user)
            checkout_details = cart_helper.prepare_cart_for_checkout()
            print(checkout_details)            
    
        except Exception as e:
            return BadRequestResponse(str(e), "Unknown", request=self.request)
        
class CampaignViewset(
    YkGenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
):
    queryset = Campaign.objects.all().order_by('id')
    serializer_class = CampaignSerializer     
   
   
         
class CouponViewset(
    YkGenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
):
    queryset = Coupon.objects.all().order_by('id')
    serializer_class = CouponSerializer
