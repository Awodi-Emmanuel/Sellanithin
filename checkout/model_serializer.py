

from dataclasses import field
from django.forms import IntegerField

from rest_framework.serializers import CharField, IntegerField, ListSerializer
from rest_framework.serializers import ModelSerializer as DrfModelSerializer
from rest_framework.utils.serializer_helpers import ReturnList
from checkout.models.implementation import BillingAddress



class MyListSerializer(ListSerializer):
    @property
    def data(self):
        ret = super().data
        return ReturnList(ret, serializer=self)
    
class ModelSerializer(DrfModelSerializer):
    class Meta:
        list_serializer_class = MyListSerializer  

class BillingAddSerializer(ModelSerializer):
    # id = IntegerField()
    
    class Meta:
        models = BillingAddress
        field = [
            'user',
            'address',
            'zipcode',
            'city', 
            'landmark'
        ]