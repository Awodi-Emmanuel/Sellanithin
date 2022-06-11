
from datetime import datetime, timedelta
from typing import Union
from uuid import uuid4

import pytz
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import validate_email as dj_validate_email
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework.fields import *
from rest_framework.serializers import Serializer, ValidationError

from core.models import TempCode

User = get_user_model()


class SignupInputSerializer(Serializer):
    username = CharField()
    first_name = CharField()
    last_name = CharField()
    phone = CharField()
    email = EmailField()
    password = CharField()
    # invite_code = CharField(required=False)

    class Meta:
        ref_name = None

    def validate_username(self, *args):
        username = self.initial_data["username"]
        u = User.objects.filter(username=username).first()
        if u: 
        #and u.date_joined >= datetime(2020, 1, 1, tzinfo=pytz.UTC):
            raise ValidationError("Username is already used.")
        return username

    def validate_email(self, *args):
        email = self.initial_data["email"]
        try:
            dj_validate_email(email)
            user = User.objects.filter(email=email).first()
            if user: 
            # and user.date_joined >= datetime(2020, 1, 1, tzinfo=pytz.UTC):
                raise ValidationError("This email already used")
        except ValidationError as e:
            raise e

        return email

    def create_user(self):
        username = self.validated_data["username"]
        email = self.validated_data["email"]
        phone = self.validated_data["phone"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        password = self.validated_data["password"]

        user = User.objects.filter(email=email).first()

        if not user:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                phone_number=phone,
                first_name=first_name,
                last_name=last_name,
            )
            user.is_active = False
            user.save()
            
        else:
            raise ValidationError("User already exist")
        
        return user
    
    
class SigninInputSerializer(Serializer):
    email = EmailField(required=False, allow_null=True)
    username = CharField(required=False, allow_null=True)
    password = CharField()
    
    class Meta:
        ref_name = None
        
    def validate_password(self, *args):
        email = self.initial_data.get("email")
        username = self.initial_data.get("username")
        password =  self.initial_data.get("password")
        
        if not email and not username:
            raise ValidationError(_("(username or email) fields should be present."))
        
        return password
    
class ConfirmInputSerializer(Serializer):
    email = EmailField()
    code = CharField()
      
    class Meta:
        ref_name = None  
        
class  ValidateOTPInputSerializer(Serializer):
    email = EmailField()
    otp = CharField()
    
    class Meta:
        ref_name = None  
        
class ResendOTPInputSerializser(Serializer):
    email = EmailField()
   
    
    class Meta:
        ref_name = None   
        
class ResendCodeInputSerializer(Serializer):
    email = EmailField()
  
    
    class Meta:
        ref_name = None                   
            