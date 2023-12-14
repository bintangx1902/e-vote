from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    category_img = models.ImageField(upload_to='goods/category/')

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_img = models.ImageField(upload_to='goods/product/')
    price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    quantity = models.IntegerField(default=0)
    description = models.TextField(default='')

    def __str__(self):
        return self.name
