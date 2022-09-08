from rest_framework import permissions
from core.pagination import MetadataPagination, MetadataPaginatorInspector
from core.custom_classes import YkGenericViewSet
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
)

from django.contrib.auth import get_user_model       
from products.models.implementation import Category, Product
from .model_serializer import (
    ProductSerializer,
    CategorySerializer
)

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

from rest_framework.decorators import action
from django.db.models import Q
from drf_yasg import openapi  # type: ignore
from drf_yasg.utils import swagger_auto_schema
from core.pagination import MetadataPagination, MetadataPaginatorInspector

from core.model_serializer import UserSerializer
User = get_user_model()

class AdminProductViewset(
    YkGenericViewSet,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
):
    permission_classes=[permissions.IsAuthenticated]
    queryset = Product.objects.all()
    pagination_class = MetadataPagination
    
    serializer_class = ProductSerializer
    
    """Create a Product function"""
    
    def post(self, request, *args, **kwargs):
        
        return self.create(request, *args, **kwargs)
    
    """Get all/list Products Function"""
    
    def get(self, request, *args, **kwargs):
        
        return self.list(request, *args, **kwargs)
     
    """Get a single Product by an id Function"""
    
    def get(self, request, *args, **kwargs):
        
        return self.retrieve(request, *args, **kwargs)
    
    """update a Product Function"""
    
    def put(self, request, *args, **kwargs):
        
        return self.update(request, *args, **kwargs)
    
    """delete a Product Function"""
    
    def delete(self, request, *args, **kwargs):
        
        return self.destroy(request, *args, **kwargs)  
                  
class CustomerProductViewset(
    YkGenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
  
):
    queryset = Product.objects.all()
    
    serializer_class = ProductSerializer
    pagination_class = MetadataPagination
    
    @swagger_auto_schema(
        operation_summary="Product",
        operation_description="Post your product",
        responses={
            200: EmptySerializer(),
            400: BadRequestResponseSerializer()
        },
        request_body=ProductSerializer(),
    )
    @action(methods=["POST"], detail=False, permission_classes=[permissions.IsAuthenticated], url_path="create")
    def create_product(self, request, *args, **kwargs):
        try:
            rcv_ser = ProductSerializer(data=self.request.data)
            if rcv_ser:
                print(rcv_ser)
                product = rcv_ser.create()
                prod_ser = UserSerializer(product)
                return GoodResponse(prod_ser.data)
            else:
                return NotFoundResponse()
        except Exception as e:
            return BadRequestResponse(str(e), "Unknown", request=self.request)
   
   
    @swagger_auto_schema(
        operation_summary="Fetch Products",
        operation_description="Fetch All Products",
        responses={
            200: EmptySerializer(),
            400: BadRequestResponseSerializer(),
        },
        # request_body=ProductSerializer()
    )
    @action(methods=["GET"], permission_classes=[permissions.IsAuthenticated], pagination_class=MetadataPagination, detail=False,)
    def get(self, request, *args, **kwargs):
        try:
            rcv_ser = ProductSerializer(data=self.request.data)
            if rcv_ser:
                product = Product.objects.all().order_by('category_id')
                serializer_class = ProductSerializer(product)
                prods_ser = serializer_class
                return GoodResponse(UserSerializer(prods_ser).data)
            else: NotFoundResponse(
                "Products not found",
                "products_error",
                request=self.request
                )
        except Exception as e:
            return BadRequestResponse(str(e), "Unknown", request=self.request)    
    
class AdminCategoryViewset(
    YkGenericViewSet,
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes=[permissions.IsAuthenticated]
    
    """Create a category function"""
    
    def post(self, request, *args, **kwargs):
        
        return self.create(request, *args, **kwargs)
    
    """Get all/list Products Function"""
    
    def get(self, request, *args, **kwargs):
        
        return self.list(request, *args, **kwargs)
     
    """Get a single category by an id Function"""
    
    def get(self, request, *args, **kwargs):
        
        return self.retrieve(request, *args, **kwargs)
    
    """update a category Function"""
    
    def put(self, request, *args, **kwargs):
        
        return self.update(request, *args, **kwargs)
    
    """delete a category Function"""
    
    def delete(self, request, *args, **kwargs):
        
        return self.destroy(request, *args, **kwargs)
    
class CustomerCategoryViewset(
    YkGenericViewSet,
    ListModelMixin,
    RetrieveModelMixin,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
 