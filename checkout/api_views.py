import math 
import random


from locale import currency
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

from core.responses import(
    CreatedResponse,
    GoodResponse,
    BadRequestResponse,
    NotFoundResponse  
)

from core.responses_serialisers import (
    EmptySerializer,
    NotFoundResponseSerializer,
    BadRequestResponseSerializer,
    
)


from cart.models.implementation import Order, Cart
from .models.implementation import BillingAddress
from .input_serializer import PaymentInputSerializer

from django.contrib.auth import get_user_model
User = get_user_model()

# import environ
# # Initialise environment variables
# env = environ.Env()
# environ.Env.read_env()
# # Create your views here.


class CheckoutViewset(YkGenericViewSet):
    @swagger_auto_schema(
        operation_summary="add payment",
        operation_description="add your payment",
        responses={
            "200": EmptySerializer(),
            "400": BadRequestResponseSerializer()
        },
    )
    @action(methods=["POST"], detail=False)

    def checkout(self, request, *args, **kwargs):
        try:
            user = User.objects.get().first()
            print("hello")
            order_qs = Order.objects.filter(user=request.user, ordered=False)
            order_items = order_qs[0].orderitems.all()
            order_total = order_qs[0].get_totals() 
            sum_items = {
                "oder_items":order_items,
                "order_total":order_total,
            }
            print(sum_items)
            
        except Exception as e:
            return BadRequestResponse(str(e), "Unknown", request=self.request)
        
        
 
class PaymentViewset(YkGenericViewSet):
    @swagger_auto_schema(
        operation_summary="Make your payment",
        operation_description="enter amout to make payment",
        responses= {
            200: EmptySerializer(),
            400: BadRequestResponseSerializer(),
        },
        request_body=PaymentInputSerializer(),
    )
    @action(methods=["POST"], detail=False)
    def payment(self, request, *args, **kwargs):
        try:
            rcv_ser = PaymentInputSerializer(data=self.request.data)
            
            if rcv_ser.is_valid():
                print(rcv_ser)
                card_number = rcv_ser.validated_data['card_number']
                cvv = rcv_ser.validated_data['cvv']
                expiry_month = rcv_ser.validated_data['expiry_month']
                expiry_year = rcv_ser.validated_data['expiry_year']
                currency = rcv_ser.validated_data['currency']
                tx_ref = rcv_ser.validated_data['tx_ref']
                fullname = rcv_ser.validated_data['fullname']
                email = rcv_ser.validated_data['email']
                amount = rcv_ser.validated_data['amount']
                phone = rcv_ser.validated_data['phone']
                
                tx_ref = {
                    "tx_ref":''+str(math.floor(1000000 + random.random()*9000000)),
                }
                # 
                # "amount":amount,
                
                data = {
                    "card_number":card_number,
                    "cvv": cvv,
                    "exipry_month": expiry_month,
                    "expiry_year": expiry_year,
                    "currency": currency,
                    "tx_ref": tx_ref,
                    "fullname": fullname,
                    "amount": amount,
                    "email": email,
                    "phone": phone
                    
                }
                
                if data:
                    print(data)
                # flutter_pro = process_payment(name, email, amount, phone)
                # if flutter_pro == rcv_ser:
                #     print(flutter_pro)
                #     return GoodResponse(flutter_pro)
        except Exception as e:
            return BadRequestResponse(str(e), "unkown", request=self.request)