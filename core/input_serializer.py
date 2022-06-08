from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.forms import CharField, EmailField
from rest_framework.serializers import Serializer

User = get_user_model()

class SignupInputSerializer(Serializer):
    username = CharField()
    first_name = CharField()
    last_name = CharField()
    email = EmailField()
    phone = CharField()
    password = CharField()
    
    class Meta:
        ref_name  = None