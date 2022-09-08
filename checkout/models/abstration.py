from tabnanny import verbose
from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.contrib.auth import get_user_model

from django.contrib.auth.models import AbstractUser

User = get_user_model()

class BillingAddress(models.Model):
    user: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE)
    address: models.CharField = models.CharField(max_length=100)
    zipcode: models.CharField = models.CharField(max_length=50)
    city: models.CharField = models.CharField(max_length=30)
    landmark: models.CharField = models.CharField(max_length=20)
    
    def __str__(self):
        return f'{self.user.username} billing address'
    
    class Meta:
        verbose_name_plural = "Billing Addresses"
        abstract = True
        
        


