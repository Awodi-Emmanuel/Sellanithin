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
    name: models.CharField = models.CharField(max_length=255)
    slug: models.CharField = models.SlugField(unique=True)
    description: models.TextField = models.TextField(blank=True, null=True)
    price: models.DecimalField = models.DecimalField(max_digits=50, decimal_places=2) 
    stock: models.IntegerField = models.IntegerField()
    available: models.BooleanField = models.BooleanField(default=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
       
    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.category,
                                               self.name,
                                               self.slug,
                                               self.description,
                                               self.price,
                                               self.stock,
                                               self.available,
                                               self.created_at,
                                               self.updated_at)   
        
        
class Cart(models.Model):
    user: models.ForeignKey = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
    item: models.ForeignKey = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity: models.IntegerField = models.IntegerField(null=False)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateField = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.user,
                                               self.item,
                                               self.quantity,
                                               self.created_at,
                                               self.updated_at)        
   
    
class DeliveryCost(models.Model):
    status: models.CharField = models.CharField(max_length=7,
                              choices=(('Active', 'active'),
                                       ('Passive', 'passive')),
                              default="passive",
                              null=False)
    cost_per_delivery: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    cost_per_product: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    fixed_cost: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DecimalField = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return "{} - {} - {} - {} - {} - {}".format(self.status,
                                                    self.cost_per_delivery,
                                                    self.cost_per_product,
                                                    self.fixed_cost,
                                                    self.created_at,
                                                    self.updated_at)
 
    
class Campaign(models.Model):
    discount_type: models.CharField = models.CharField(max_length=6,
                                     choices=(('Amount', 'amount'), ('Rate', 'rate')),
                                     default="rate",
                                     null=False)
    discount_rate: models.IntegerField = models.IntegerField(null=True, blank=True)
    discount_amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    min_purchased_items: models.IntegerField = models.IntegerField(null=False)
    apply_to: models.CharField = models.CharField(max_length=8,
                                choices=(('Product', 'product'), ('Category', 'category')),
                                default="product",
                                null=False)
    target_product: models.ForeignKey = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    target_category: models.ForeignKey = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "{} - {} - {} - {} - {} - {} - {} - {} - {}".format(self.discount_type,
                                                                   self.discount_rate,
                                                                   self.discount_amount,
                                                                   self.min_purchased_items,
                                                                   self.apply_to,
                                                                   self.target_product,
                                                                   self.target_category,
                                                                   self.created_at,
                                                                   self.updated_at)    
        
        
class Coupon(models.Model):
    minimum_cart_amount: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    discount_rate: models.IntegerField = models.IntegerField(null=False)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "{} - {} - {} - {}".format(self.minimum_cart_amount,
                                          self.discount_rate,
                                          self.created_at,
                                          self.updated_at)        