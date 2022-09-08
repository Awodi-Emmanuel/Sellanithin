from datetime import datetime, timedelta
import email
from locale import currency
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


class PaymentInputSerializer(Serializer):
    card_number = CharField()
    cvv = CharField()
    expiry_month = CharField()
    expiry_year = CharField()
    currency = CharField()
    tx_ref = CharField()
    fullname = CharField()
    email = EmailField()
    phone= CharField()
    amount = FloatField()

    class Meta:
        ref_name = None