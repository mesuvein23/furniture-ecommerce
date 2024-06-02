from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from vendor.models import *

class Contact(models.Model):
    fname = models.CharField(max_length=50) 
    lname = models.CharField(max_length=50) 
    email = models.EmailField(max_length=254)   
    phone = models.BigIntegerField()
    message = models.TextField()

    def __str__(self):
        return self.fname + 'by' + self.lname
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_quantity =models.IntegerField(null=False, blank=False, default="True")
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total(self):
        price = self.product.selling_price
        quantity = self.cart_quantity
        total = price*quantity
        return total

class Order(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    fname = models.CharField(max_length=150, null = False)
    lname = models.CharField(max_length=150, null = False)
    email = models.CharField(max_length=150, null = False)
    phone = models.CharField(max_length=150, null = False)
    address = models.CharField(max_length=150, null = False)
    city = models.CharField(max_length=150, null = False)
    state = models.CharField(max_length=150, null = False)
    country = models.CharField(max_length=150, null = False)
    zipcode = models.CharField(max_length=150, null = False)
    total_price = models.FloatField(null=False)
    payment_mode = models.CharField(max_length=150, null=False)
    payment_id = models.CharField(max_length=200, null=True)
    orderstatuses = (
        ('Pending', 'Pending'),
        ('Out For Shipping', 'Out For Shipping'),
        ('Completed','Completed'),
    )
    status = models.CharField(max_length=150,choices=orderstatuses, default='Pending')
    message=models.TextField(null=True)
    tracking_no = models.CharField(max_length=150, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.id, self.tracking_no)
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField(null=False)    
    quantity = models.IntegerField(null=False, default=False)

    def __str__(self):
        return '{} {}'.format(self.order.id, self.order.tracking_no , self.product)
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)    
    phone = models.CharField(max_length=50, null=False)
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    zipcode = models.CharField(max_length=150, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
