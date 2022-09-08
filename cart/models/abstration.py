from django.db import models
# from products.models.abstration import Category
from products.models.implementation import Product, Category
from core.models.implementation import Users


        
class Cart(models.Model):
    user: models.ForeignKey = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True)
    item: models.ForeignKey = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    quantity: models.IntegerField = models.IntegerField(null=False)
    purchased: models.BooleanField = models.BooleanField(default=False)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateField = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        abstract = True

    def __str__(self):
        return "{} - {} - {} - {} - {}".format(self.user,
                                               self.item,
                                               self.quantity,
                                               self.purchased,
                                               self.created_at,
                                               self.updated_at)
        
    def get_total(self):
        total = self.item.price * self.quantity
        floattotal = float("{0.0f}".format(total))
        return floattotal        


class Order(models.Model):
    orderitems: models.ManyToManyField = models.ManyToManyField(Cart)
    user: models.ForeignKey = models.ForeignKey(Users, on_delete=models.CASCADE)
    ordered: models.BooleanField = models.BooleanField(default=False)
    created: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    paymentId: models.CharField = models.CharField(max_length=200, blank=True, null=True)
    orderId: models.CharField = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        abstract = True
    
    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0 
        for ordered_item in self.orderitems:
            total += ordered_item.get_total()
            
        return total
    
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