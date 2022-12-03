from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug>', Categories.as_view(), name='category'),
    path('product-detail/<slug>', ProductView.as_view(), name='product-detail'),
    path('reviews', reviews, name='reviews'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/<slug>', add_to_cart, name='add_to_cart'),
    path('delete_cart/<slug>', delete_cart, name='delete_cart'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('add_to_wishlist/<slug>', add_to_wishlist, name='add_to_wishlist'),
    path('delete_wishlist/<slug>', delete_wishlist, name='delete_wishlist'),
]
