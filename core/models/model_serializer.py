from dataclasses import field
from rest_framework.serializers import CharField, IntegerField, ListSerializer
from rest_framework.serializers import ModelSerializer

from core.models.abstration import Category, Product 

class CategorySerializer(ModelSerializer):
    id = IntegerField()
    
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "slug"
        )   

class ProductSerializer(ModelSerializer):
    id = IntegerField()
    
    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "name",
            "slug",
            "description",
            "price",
            "image",
            "thumbnail",
            "stock",
            "available",
        )
        