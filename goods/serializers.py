from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation['category_img'] is not None:
	    representation['category_img'] = representation['category_img'].replace('https', 'http')
        return representation


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
	if representation['product_img'] is not None:
	    representation['product_img'] = representation['product_img'].replace('https', 'http')
        return representation


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
