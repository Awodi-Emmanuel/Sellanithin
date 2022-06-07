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

from core.models.abstration import Category, Product
from core.models.model_serializer import ProductSerializer, CategorySerializer


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