from email import message
import logging

import traceback
from pytz import timezone

from requests import request
from core.models.abstration import DeliveryCost

from core.pagination import MetadataPagination, MetadataPaginatorInspector
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.authtoken.models import Token
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

from core.models.implementation import Category, Product, Cart, DeliveryCost
from core.model_serializer import(
    ProductSerializer,
    CategorySerializer,
    UserSerializer,
    CartSerailizer
)
from core.models import TempCode, Category

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
from core.errors import BadRequestError, NotFoundError


from .input_serializer import(
    SigninInputSerializer,
    SignupInputSerializer,
    ConfirmInputSerializer,
    ValidateOTPInputSerializer,
    ResendOTPInputSerializser,
    ResendCodeInputSerializer,
    ResetInputSerializer,
    ResetWithPasswordSerializer,
    ChangePasswordSerializer
)

from .cart_helper import CartHelper, DeliveryCostHelper
from Ecom import settings
from utils import base, crypt

from producer.notification_producer import (
    ChannelType,
    NotificationProducer,
    NotificationType
)

logger = logging.getLogger()

User = get_user_model()


class AuthViewset(
    YkGenericViewSet, 
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,):
    def get_queryset(self):
        user = User.objects.all()
        return user
    
    serializer_class = UserSerializer()
    
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
                    code = "12345"  # TODO: Create and add code generation function
                    code_otp = "546387"
                    fe_url = settings.FRONTEND_URL
                    TempCode.objects.create(code=code, user=user, type="signup")
                    TempCode.objects.create(code=code_otp, user=user, type="signup_otp")
                    confirm_url = (
                        fe_url
                        + f"/confirm?code={crypt.encrypt(code)}&firstname={crypt.encrypt(user.first_name)}&lastname={crypt.encrypt(user.last_name)}&email={crypt.encrypt(user.email)}"
                    )
                    message = {
                        "subject": _("Confirm Your Email"),
                        "email": user.email,
                        "confirm_url": confirm_url,
                        "username": user.username,
                    }
                   
                    NotificationProducer(
                        req_id="halkjhdflkjfdlkjhg",
                        stream_id="hkajdfhjgkhgjhk",
                        channel=[ChannelType.mail.value],
                        notification_type=NotificationType.signup.value,
                        message=message,
                    ).send_notification_event()
                   
                    message = {
                        "subject": _("Confirm Your Email"),
                        "phone": user.phone_number,
                        "code": code_otp,
                        "username": user.username,
                    }
                    
                    NotificationProducer(
                        req_id="halkjhdflkjfdlkjhg",
                        stream_id="hkajdfhjgkhgjhk",
                        channel=[ChannelType.sms.value],
                        notification_type=NotificationType.signup.value,
                        message=message,
                    ).send_notification_event()
                    
                    return CreatedResponse({"message": "user created"})
                
                return GoodResponse()
            else:
                return BadRequestResponse(
                    "Unable to signup",
                    "signup_error",
                    data=rcv_ser.errors,
                    request=self.request,
                )
        except Exception as e:
            logger.error(traceback.print_exc())
            return BadRequestResponse(str(e), code="unknown", request=self.request)      
        
    @swagger_auto_schema(
        operation_summary="Confirm",
        operation_description="Confirm your email",
        responses={
            200: EmptySerializer(),
            400: BadRequestResponseSerializer(),
            404: NotFoundResponseSerializer(),
        },
        request_body=ConfirmInputSerializer()
    )
    @action(methods=["POST"], detail=False,)
    
    def confirm(self, request, *args, **kwargs):
        try:
            rcv_seria = ConfirmInputSerializer(data=self.request.data)
            if rcv_seria.is_valid():
                tmp_code = (
                    TempCode.objects.filter(
                        code=crypt.encrypt(rcv_seria._validated_data["code"]),
                        user__email=crypt.encrypt(rcv_seria.validated_data["email"]),
                        is_used = False,
                        expires__gte=timezone.now(),
                    )
                    .select_related()
                    .first()
                )
                if tmp_code:
                    tmp_code.user.email_is_verified = True
                    tmp_code.user.save()
                    tmp_code.is_used = True
                    tmp_code.save()
                    
                    user_ser = UserSerializer(tmp_code.user)
                    
                    message = {
                        "subject": _("Welcome To ecoms"),
                        "email": tmp_code.user.email,
                        "username": tmp_code.user.username
                    }
                    
                    NotificationProducer(
                        req_id = "halkjhdflkjfdlkjhg",
                        stream_id ="hkajdfhjgkhgjhk",
                        channel=[ChannelType.mail.value],
                        notification_type=NotificationType.confirm.value,
                        message=message
                    ).send_notification_event()
                    
                    return GoodResponse(user_ser.data)
                else:
                    return NotFoundResponse(
                        "TempCode not found or invalid",
                        "TempCode",
                        request=self.request
                    )
            else:
                return BadRequestResponse(
                    "Unable to confirm",
                    "confirm_error",
                    request=self.request,
                )
        except Exception as e:
            logger.error(traceback.print_exc())
            return BadRequestResponse(str(e), "Unkonwn", request=self.request) 
        
        
    @swagger_auto_schema(
        operation_summary="Validate Otp",
        operation_description="Validate your OTP",
        responses={
            200: EmptySerializer(),
            400: BadRequestResponseSerializer(),
            404: NotFoundResponseSerializer(),
        },
        request_body=ValidateOTPInputSerializer(),
    )         
    @action(methods=["POST"], detail=False, url_path="validate/otp")
    
    def validate_otp(self, request, *args, **kwargs):
        try:
            rcv_ser = ValidateOTPInputSerializer(data=self.request.data)
            if rcv_ser.is_valid():
                tmp_code = (
                    TempCode.objects.filter(
                        code= crypt.decrypt(rcv_ser.validated_data["otp"]),
                        user__email = crypt.decrypt(rcv_ser.validated_data["email"]),
                        is_used = False,
                        expires__gte=timezone.now()
                    )
                    .select_related()
                    .first()
                )
                
                if tmp_code:
                    tmp_code.user.is_active = True
                    tmp_code.user.save()
                    tmp_code.user.is_used = True
                    tmp_code.save()
                    
                    user_ser = UserSerializer(tmp_code.user)
                    
                    return GoodResponse(user_ser.data)
                
                else:
                    return NotFoundResponse("OTP not found or invalid", "OTP", request=self.request)
                
            else:
                return BadRequestResponse(
                    "Unable to validate OTP",
                    "otp_validation_error",
                    data=rcv_ser.errors,
                    request=self.request,
                )   
        except Exception as e:
            return BadRequestResponse(str(e), "Uknown", request=self.request)
        
        
    @swagger_auto_schema(
        operation_summary="Resend",
        operation_description="Resend code",
        responses={
            200: EmptySerializer(),
            400: BadRequestResponseSerializer(),
            404: NotFoundResponseSerializer(),
        },
        request_body=ResendOTPInputSerializser(),
    )      
    @action(methods=["POST"], detail=False, url_path="resend/otp")
    
    def resend_otp(self, request, *args, **kwargs):
        try:
            rcv_ser = ResendOTPInputSerializser(data=self.request.data)
            
            if rcv_ser.is_valid():
               
                user = User.objects.filter(
                    email = rcv_ser.validated_data["email"],
                    is_active = False
                ).first()
                
                if user:
                    tmp_codes = TempCode.objects.filter(
                        user__email=rcv_ser.validated_data["email"],
                        is_used = False,
                        expires__gte= timezone.now()
                    ).select_related()
                    
                    tmp_codes.update(is_used=True)
                    
                    try:
                        tmp_codes.save()
                        
                    except:
                        pass
                    
                    code = "54321"
                    TempCode.objects.create(code=code, user=user, type="resend_otp")
                    
                    message = {
                        "email": user.email,
                        "username": user.username
                    }
                    
                    # TODO Create Apache Kafka Notification
                    
                    return GoodResponse({"Confirmation email sent"})
                else:
                    return NotFoundResponse(
                        "User is active or User not found",
                        "user_is_active",
                        request=self.request,
                    )
            else:
                return BadRequestResponse(
                    "Invalid data sent",
                    "invalid_data",
                    data=rcv_ser.errors,
                    request=self.request
                )
        except Exception as e:
            return BadRequestResponse(str(e), "Unknown", request=self.request)
        
        
    @swagger_auto_schema(
        operation_summary="Resend Email",
        operation_description="Resend Confirmation Email",
        responses={
            200: EmptySerializer(),
            400: BadRequestResponseSerializer(),
            404: NotFoundResponseSerializer(),
        },
        request_body=ResendCodeInputSerializer(),
    )
    @action(methods=["POST"], detail=False, permission_classes=[permissions.IsAuthenticated])
    
    
    def resend(self, request, *args, **kwargs):
        try:
            rcv_ser = ResendCodeInputSerializer(data=self.request.data)
            if rcv_ser.is_valid():
                user = self.request.user
                if user.email_is_verified:
                    return BadRequestResponse(
                        "User is already activated",
                        "user_is_active",
                        data=rcv_ser.errors,
                        request=self.request,
                    )
                tmp_codes = TempCode.objects.filter(
                    user__email=rcv_ser.validated_data["email"],
                    is_used = False,
                    expires__gte = timezone.now(),
                ).select_related()
                    
                code = "54672" 
                fe_url = settings.FRONTEND_URL
                TempCode.objects.filter(
                    code=code, user=user, type="resend_confirmation"
                )
                
                confirm_url = (
                    fe_url
                    + f"/confirm?code={base.url_safe_encode(code)}&firstname={base.url_safe_encode(user.first_name)}&lastname={base.url_safe_encode(user.last_name)}&email={base.url_safe_encode(user.email)}"
                )
                print(confirm_url)
                    
                message = {
                    "subject": _("Confirm Your Email"),
                    "email": self.request.user.email,
                    "confirm_url": confirm_url,
                    "username": self.request.user.username
                }
                    
                # TODO Create Apache Kafka Notification
                
                tmp_codes.update(is_used=True)
                    
                try:
                    tmp_codes.save()
                except:
                    pass
                    
                return GoodResponse({
                    "Confirmation email sent",
                        
                })                        
            
            else:
                return BadRequestResponse(
                    "Invalid data sent",
                    "invalid_data",
                    data=rcv_ser.errors,
                    request=self.request,
                )
            
        except Exception as e:
            return BadRequestResponse(str(e), "Unknown", request=self.request) 
        
    @swagger_auto_schema(
        operation_summary="signin",
        operation_description="signin with your email",
        responses={
            200: EmptySerializer(),
            400: BadRequestResponseSerializer(),
            404: NotFoundResponseSerializer(),
        },
        request_body=SigninInputSerializer(),
    )
    
    @action(methods=["POST"], detail=False,)
    
    def signin(self, request, *args, **Kwargs):
        try:
            rcv_ser = SigninInputSerializer(data=self.request.data)
            if rcv_ser.is_valid():
                email = rcv_ser.validated_data.get("email")
                username = rcv_ser.validated_data.get("username")
                password = rcv_ser.validated_data["password"]
                user = User.objects.filter(
                    Q(email=email) | Q(username=username)
                ).first() 
                if user:
                    if user.is_active:
                        if user.check_password(password):
                            cookie = UserSerializer().get_tokens(user)
                            print(cookie)
                            return GoodResponse(
                                UserSerializer(user).data, cookie=cookie
                            )
                        else:
                            return BadRequestResponse(
                                "Invalid email/password credentials",
                                "invalid_credentials",
                                request=self.request,
                            )
                    else:
                        return BadRequestResponse(
                            "User is not active", "user_inactive", request=self.request,
                        )
                            
                else:
                    return BadRequestResponse(
                        "Invalid email/password credentials",
                        "invalid_credentials",
                        request=self.request,
                    )
            else: 
                return BadRequestResponse(
                    "Unable to signin",
                    "signin_error",
                    data=rcv_ser.errors,
                    request=self.request,
                )
        except Exception as e:
            traceback.print_exc()
            return BadRequestResponse(str(e), "Unknown", request=self.request)
        
        
        
    @swagger_auto_schema(
        operation_summary="signout",
        operation_description="Signout",
        responses={
            200: EmptySerializer(),
            400: BadRequestResponseSerializer(),
        },
    )
    @action(methods=["methods"], detail=False, permission_classes=[permissions.IsAuthenticated])
    
    def signout(self, request, *args, **kwargs):
        try:
            logout(self.request)
            return GoodResponse({})
        except Exception as e:
            return BadRequestResponse(str(e), "Unknown", request=self.request)   
        
    @swagger_auto_schema(
        operation_summary="Reset init",
        operation_description="Init the reset password",
        responses={
            200: EmptySerializer(),
            400: BadRequestResponseSerializer(),
            404: NotFoundResponseSerializer(),
        },
        request_body=ResetInputSerializer(),
    )
    @action(methods=["POST"], detail=False, url_path="reset/init")
    
    def reset_init(self, request, *args, **kwargs):
        try:
            rcv_ser = ResetInputSerializer(data=self.request.data)
            if rcv_ser.is_valid():
                email = rcv_ser.validated_data.get("email")
                user = User.objects.filter(email=email).first()
                
                if user:
                    code = "12345"
                    TempCode.objects.create(
                        code=code, user=user, type="reset"
                    )
                    
                    email_encoded = base.url_safe_encode(user.email)
                    code_encoded = base.url_safe_encode(code)
                    
                    fe_url = settings.FRONTEND_URL
                    confirm_url = (
                        fe_url
                        + f"/reset?token={code_encoded}&email={email_encoded}"
                    )
                    
                    messge = {
                        "subject": _("confirm you email"),
                        "email": user.email,
                        "reset_url": confirm_url,
                        "user": user.username,
                    }
                    
                    # TODO Create Apache Kafka Notification
                    return GoodResponse({
                        "successful"
                    })
            else:
                return BadRequestResponse(
                    "Unable to init the password reset",
                    "init_reset_error",
                    request=self.request
                )
                
        except Exception as e:
            return BadRequestResponse(str(e), "Unkonwn", request=self.request) 
        
    @swagger_auto_schema(
        operation_summary="Reset Code Check",
        operation_description="Check if the reset code is valid",
        responses={
            200: EmptySerializer(),
            400: BadRequestResponseSerializer(),
            404: NotFoundResponseSerializer(),
        },
        request_body=ConfirmInputSerializer(),
    )           
    @action(methods=["POST"], detail=False, url_path="reset/validate/token")
    
    def reset_password_validate_token(self, request, *args, **kwargs):
        try:
            rcv_ser = ConfirmInputSerializer(data=self.request.data)
            if rcv_ser.is_valid():
                email: str = rcv_ser.validated_data["email"]
                code: str = rcv_ser.validated_data["code"]
                
                token_decoded =  base.url_safe_decode(code)
                email_decoded = base.url_safe_decode(email)
                
                tmp_codes = (
                    TempCode.objects.filter(
                        code=token_decoded,
                        user__email=email_decoded,
                        is_used=False,
                        expires__gte=timezone.now() 
                    )
                    .select_related()
                    .first()
                )
                
                if tmp_codes:
                    tmp_codes.user.is_active = False
                    tmp_codes.user.save()
                    user_ser = UserSerializer(tmp_codes.user)
                    return GoodResponse(user_ser.data)
                else:
                    return NotFoundResponse(
                        "Expired or Invalid Token", "InvalidToken", request=self.request
                    )
            else: 
                return BadRequestResponse(
                    "Unable to check reset code",
                    "invalid_data",
                    data=rcv_ser.errors
                )
                        
        except Exception as e:
            return BadRequestResponse(str(e), "Unknown", request=self.request)
         
        
    @swagger_auto_schema(
        operation_summary="Reset",
        operation_description="Reset your password",
        responses={
            200: EmptySerializer(),
            400: BadRequestResponseSerializer(),
            404: NotFoundResponseSerializer(),
        },
        request_body=ResetWithPasswordSerializer(),
    )
    
    @action(methods=["POST"], detail=False, url_path="reset/complete")
    
    def reset_password_complete(self, request, *args, **kwargs):
        try:
            rcv_ser = ResetWithPasswordSerializer(data=self.request.data)
            if rcv_ser.is_valid():
                code = base.url_safe_decode(rcv_ser.validated_data["code"])
                email = base.url_safe_decode(rcv_ser.validated_data["email"])
                tmp_code = (
                    TempCode.objects.filter(
                        code=code,
                        user__email=email,
                        is_used=False,
                        expires__gte=timezone.now()
                    )
                    .select_related()
                    .first()
                )
                if tmp_code:
                    tmp_code.user.is_active=True
                    tmp_code.user.set_password(rcv_ser.validated_data["email"])
                    tmp_code.user.save()
                    tmp_code.is_used=True
                    tmp_code.save()
                    
                    tpl = "reset"
                    message = {
                        "subject": _("Password reset confirmation"),
                        "tpl": tpl
                    }
                    
                    # TODO Create Apache Kafka Notification
                    
                    user_ser = UserSerializer(tmp_code.user)
                    return GoodResponse(user_ser.data)
                else:
                    return NotFoundResponse(
                        "Token expired or invalid",
                        "invalid_data",
                        request=self.request,
                    )
            else:
                return BadRequestResponse(
                    "Unable to reset",
                    "invalid_data",
                    request=self.request
                ) 
        except Exception as e:
            return BadRequestResponse(str(e), "Unknown", request=self.request)
        
    @swagger_auto_schema(
        operation_summary="Change Password",
        operation_description="Change user's password",
        responses={
            200: UserSerializer(),
            400: BadRequestResponseSerializer(),
            404: NotFoundResponseSerializer(),
        },
        request_body=ChangePasswordSerializer(),
    )
    @action(methods=["POST"], detail=False, permission_classes=[permissions.IsAuthenticated], url_path="password/change",)
    
    def Change_password(self, request, *args, **kwargs):
        try:
            rcv_ser = ChangePasswordSerializer(data=self.request.data)
            
            if rcv_ser.is_valid():
                old_password = rcv_ser.validated_data["old_password"]
                new_password = rcv_ser.validated_data["new_password"]
                confirmed_password = rcv_ser.validated_data["confirmed_password"]
                
                if self.request.user.check_password(old_password):
                    if new_password == confirmed_password:
                        self.request.user.set_password(new_password)
                        self.request.user.save()
                        
                        message = {
                            "subject": _("Your Password was Changed"),
                            "email": self.request.user.email,
                            "username": self.request.user.username
                        }
                        
                        # TODO Create Apache Kafka Notification
                        
                        return GoodResponse(UserSerializer(self.request.user).data)
                    else:
                        return BadRequestError(
                            "New passwords are differents",
                            "new_password_different",
                            self.request,
                        ) 
                else:
                    return BadRequestError(
                        "The old password is invalid",
                        "old_invalid_password",
                        self.request,
                    ) 
            else:
                return BadRequestResponse(
                    "Unable to reset",
                    "reset_error",
                    data=rcv_ser.errors,
                    request=self.request,
                )                              
        except Exception as e:
            return BadRequestResponse(str(e), "Uknown", request=self.request)  
        
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
    @action(permission_classes=[permissions.IsAuthenticated], detail=False,)
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
        
        
        
class  CartViewset(
    YkGenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,):
    queryset = Cart.objects.all().order_by('id')
    serializer_class = CartSerailizer
    
    @swagger_auto_schema(
        operation_summary="Cart",
        operation_description="Add to card",
        responses={
            200: EmptySerializer(),
            400: BadRequestResponseSerializer(),
        },
    )
    @action(methods=["get"], detail= False, url_path='checkout/(?P<userId>[^/.]+)', url_name='checkout')
    def checkout(self, request, *args, **kwargs):
        try:
            user = User.objects.get(pk=int(kwargs.get('userId'))) 
            cart_helper = CartHelper(user)
            checkout_details = cart_helper.prepare_cart_for_checkout()
            print(checkout_details)            
    
        except Exception as e:
            return BadRequestResponse(str(e), "Unknown", request=self.request)
       
        
