from django.urls import path
from .views import *

urlpatterns = [
    path('category',CategoryListEndPoint.as_view(),name='category-list'),
    path('product', ProductListEndPoint.as_view(), name='product-list'),
]