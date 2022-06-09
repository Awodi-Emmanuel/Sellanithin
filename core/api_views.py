from email import message
import logging
# from math import perm
import traceback

from requests import request
from core.custom_classes import YkGenericViewSet
from rest_framework.views import APIView
from django.contrib.auth import login, logout
import logging
from django.utils.translation import gettext as _
from rest_framework import permissions
from uuid import uuid4
from datetime import timedelta, datetime
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
)

from django.contrib.auth import get_user_model

from core.models.implementation import Category, Product
from core.model_serializer import(
    ProductSerializer,
    CategorySerializer,
    UserSerializer,
)
from core.models import TempCode

from rest_framework.decorators import action
from django.db.models import Q
from drf_yasg import openapi  # type: ignore
from drf_yasg.utils import swagger_auto_schema  # type: ignore

from .responses_serialisers import (
    EmptySerializer,
    NotFoundResponseSerializer,
    BadRequestResponseSerializer,
    
)

from .responses import(
    CreatedResponse,
    GoodResponse,
    BadRequestResponse,
    NotFoundResponse  
)

from .input_serializer import(
    SignupInputSerializer
)

from Ecom import settings
from utils import base, crypt

logger = logging.getLogger()

User = get_user_model()

class AuthViewset(YkGenericViewSet):
    queryset = User.objects.all()
    
    serializer = UserSerializer
    
    
    @swagger_auto_schema(
        operation_summary="Signup",
        operation_description="Signup using your email",
        responses={200: EmptySerializer(), 400: BadRequestResponseSerializer()},
        request_body=SignupInputSerializer(),
    )    

    @action(methods=["POST"], detail=False)
    def signup(self, request, *args, **kwargs):
        try:
            rcv_ser = SignupInputSerializer(data=self.request.data)
            if rcv_ser.is_valid():
                user = rcv_ser.create_user()
                if not user.is_active:
                    code = "12345"
                    code_otp = "546387"
                    
                    fe_url = settings.FRONTEND_URL
                    TempCode.objects.create(code=code, user=user, type="signup")
                    TempCode.objects.create(code_otp=code_otp, user=user, type="signup")
                    
                    confirm_url = (
                        fe_url 
                        + f"/confirm?code={crypt.encrypt(code)}&firstname={crypt.encrypt(user.first_name)}&lastname={crypt.encrypt(user.last_name)}&email={crypt.encrypt(user.email)}"
                    )
                    
                    message = {
                        "subject": _("Confirm you Email"),
                        "email": user.email,
                        "confirm_url": confirm_url,
                        "code": code_otp,
                        "username": user.username,
                    }
                    # TODO: Create Apache Kafka
                    
                    message = {
                        "subject": _("Confirm Your Email"),
                        "phone": user.email,
                        "code": code_otp,
                        "username": user.username
                    }
                    
                    # TODO: Create Apache Kafka
                else:
                    return CreatedResponse({"message": "User created"})
            else:
                return BadRequestResponse(
                        "Unable to confirm",
                        "confirm_error",
                        request=self.request,
                    )
        except Exception as e:
            logger.error(traceback.print_exc())
            return BadRequestResponse(str(e), "Uknown", request=self.request)            



class ProductViewset(
    YkGenericViewSet,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
):
    queryset = Product.objects.all()
    
    serializer_class = ProductSerializer
    
    """Create a Product function"""
    
    # def post(self, request, *args, **kwargs):
        
    #     return self.create(request, *args, **kwargs)
    
    # """Get all/list Products Function"""
    
    # def get(self, request, *args, **kwargs):
        
    #     return self.list(request, *args, **kwargs)
     
    # """Get a single Product by an id Function"""
    
    # def get(self, request, *args, **kwargs):
        
    #     return self.retrieve(request, *args, **kwargs)
    
    # """update a Product Function"""
    
    # def put(self, request, *args, **kwargs):
        
    #     return self.update(request, *args, **kwargs)
    
    # """delete a Product Function"""
    
    # def delete(self, request, *args, **kwargs):
        
    #     return self.destroy(request, *args, **kwargs)
    
    
class CategoryViewset(
    YkGenericViewSet,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
):
    queryset = Category.objects.all()
    
    serializer_class = CategorySerializer