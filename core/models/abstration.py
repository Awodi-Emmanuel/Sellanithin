from django.db import models
from io import BytesIO
from PIL import Image
from django.core.files import File
from django.contrib.auth.models import AbstractUser



class Users(AbstractUser):
    email_is_verified: models.BooleanField = models.BooleanField(default=False)
    country: models.CharField = models.CharField(max_length=50)
    address: models.CharField = models.CharField(max_length=255)
    city: models.CharField = models.CharField(max_length=255)
    state: models.CharField = models.CharField(max_length=255, null=True, blank=True)
    phone_number: models.CharField = models.CharField(max_length=20)
    contact_name: models.CharField = models.CharField(max_length=255)
    
    REQUIRED_FIELDS = [
        'phone_number'
    ]
    class Meta:
        abstract = True  
    
class TempCode(models.Model):
    TYPES = [
        ("signin", "signin"),
        ("signup", "signup"),
        ("reset", "reset"),
        ("resend_confirmation", "resend_confirmation"),    
    ]  
    
    code: models.CharField = models.CharField(max_length=255)
    type: models.CharField = models.CharField(max_length=50, choices=TYPES)
    created: models.DateField = models.DateField(auto_now_add=True)
    expires: models.DateField = models.DateField()
    is_used: models.BooleanField = models.BooleanField(default=False)
    user: models.ForeignKey = models.ForeignKey(Users, models.CASCADE) 
    
    class Meta:
        abstract = True 
    

# Create your models here.
class Category(models.Model):
    name: models.CharField = models.CharField(max_length=255)
    parent_category_id: models.IntegerField = models.IntegerField(null=True, blank=True)
    slug: models.SlugField = models.SlugField(unique=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
      
    def __str__(self):
        return "{} - {} - {} - {}".format(self.name,
                                          self.slug,
                                          self.parent_category_id,
                                          self.created_at,
                                          self.updated_at)                
    
                            
class Product(models.Model):
    category: models.ForeignKey = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    name: models.CharField(max_length=255)
    slug: models.CharField = models.SlugField(unique=True)
    description: models.TextField = models.TextField(blank=True, null=True)
    price: models.DecimalField = models.DecimalField(max_digits=50, decimal_places=2) 
    stock: models.IntegerField = models.IntegerField()
    available: models.BooleanField = models.BooleanField(default=True)
    date_added: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
       
    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.category,
                                               self.title,
                                               self.price,
                                               self.created_at,
                                               self.updated_at)   
    