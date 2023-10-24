from django.contrib import admin
from django.urls import path
from .views import PRODUCTMODELVIEW


urlpatterns = [
    path('create/', PRODUCTMODELVIEW.as_view()),
]