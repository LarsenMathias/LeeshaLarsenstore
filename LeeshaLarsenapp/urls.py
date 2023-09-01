from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns=[
    path('checkout',checkout,name='checkout'),
    path('cart',cart,name='cart'),
    path('home',home,name='home'),
    path('login',user_login,name='login'),
    path('update_item',updateItem,name='update_item'),
     path("register", signup, name="register"),
     path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
]