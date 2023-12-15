from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinValueValidator
from django.db import models
from os import path, remove
from django.conf import settings


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    category_img = models.ImageField(upload_to='goods/category/', blank=True, null=True, default='dummy/dummy.jpg')

    def __str__(self):
        return f"{self.name}"

    def delete(self, using=None, *args, **kwargs):
        if not self.category_img or ('dummy' in f"{self.category_img}"):
            try:
                file_path = path.join(settings.MEDIA_ROOT, self.category_img.name)
                if path.isfile(file_path):
                    remove(file_path)
            except ObjectDoesNotExist as e:
                print(f"file does not exist : {e}")
        return super().delete(using=None, *args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_img = models.ImageField(upload_to='goods/product/', blank=True, null=True, default='dummy/dummy.jpg')
    price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    quantity = models.IntegerField(default=0)
    description = models.TextField(default='')

    def __str__(self):
        return self.name

    def delete(self, using=None, *args, **kwargs):
        try:
            file_path = path.join(settings.MEDIA_ROOT, self.product_img.name)
            if path.isfile(file_path):
                remove(file_path)
        except ObjectDoesNotExist as e:
            print(f"file does not exist : {e}")
        return super().delete(using=None, *args, **kwargs)
