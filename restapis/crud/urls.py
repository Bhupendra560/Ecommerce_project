from django.contrib import admin
from django.urls import path
from .views import PRODUCTMODELVIEW


urlpatterns = [
    path('add/', PRODUCTMODELVIEW.as_view(), name='add new product'),
    path('get/', PRODUCTMODELVIEW.as_view(), name='get all products'),
    path('get/<int:pk>/', PRODUCTMODELVIEW.as_view(), name='get product'),
    path('update/<int:pk>/', PRODUCTMODELVIEW.as_view(), name='update product'),
    path('delete/<int:pk>/', PRODUCTMODELVIEW.as_view(), name='delete product')
]