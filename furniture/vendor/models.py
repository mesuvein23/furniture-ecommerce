from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
# Create your models here.

class Base(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+",db_column="created_by",null=True)
    created_at = models.DateTimeField(null=True)
    updated_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name="+",db_column="updated_by",null=True)
    updated_at = models.DateTimeField(null=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Category(Base):
    slug = models.CharField(max_length=50, default="")
    name = models.CharField(max_length=50, default="")
    image = models.ImageField(upload_to='images/' , null=True, default="")

    class Meta:
        db_table = 'category'

    def __str__(self):
        return self.name



class Product(Base):
    title = models.CharField(max_length=50)
    category= models.ForeignKey(Category, on_delete=models.CASCADE) 
    description = HTMLField()
    image = models.ImageField(upload_to='images/' , null=True, default="")
    quantity =models.IntegerField(null=False, default=False)
    slug = models.CharField(max_length=50)
    marked_price = models.IntegerField()
    selling_price = models.IntegerField()
    new_arrivals = models.BooleanField(default="")
    top_selling = models.BooleanField(default="")
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        db_table = "product"

    def __str__(self):
        return self.title


