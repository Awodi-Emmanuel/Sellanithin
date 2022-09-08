from rest_framework.serializers import CharField, IntegerField, ListSerializer
from rest_framework.serializers import ModelSerializer as DrfModelSerializer
from rest_framework.utils.serializer_helpers import ReturnList

from .models.implementation import (
    Category,
    Product
)

class MyListSerializer(ListSerializer):
    @property
    def data(self):
        ret = super().data
        return ReturnList(ret, serializer=self)
    
class ModelSerializer(DrfModelSerializer):
    class Meta:
        list_serializer_class = MyListSerializer  


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
            "updated_at"
        )
        
