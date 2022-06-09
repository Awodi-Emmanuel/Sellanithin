from cmath import e
import logging
# from math import perm
import traceback

from requests import request

from core.custom_classes import YkGenericViewSet
from rest_framework.views import APIView
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
    GoodResponse,
    BadRequestResponse,
    NotFoundResponse  
)

from .input_serializer import(
    SignupInputSerializer
)


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
                    
                else:
                    print("hello")
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