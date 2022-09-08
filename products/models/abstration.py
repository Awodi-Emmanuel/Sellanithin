from django.db import models
from core.models.implementation import Users


# Create your models here.
class Category(models.Model):
    name: models.CharField = models.CharField(max_length=255)
    parent_category_id: models.IntegerField = models.IntegerField(null=True, blank=True)
    slug: models.SlugField = models.SlugField(unique=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
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
    slug: models.SlugField = models.SlugField(max_length=225)
    description: models.TextField = models.TextField(blank=True, null=True)
    price: models.DecimalField = models.DecimalField(max_digits=50, decimal_places=2) 
    stock: models.IntegerField = models.IntegerField()
    available: models.BooleanField = models.BooleanField(default=True)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

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
        
