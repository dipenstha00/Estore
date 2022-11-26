from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug>', Categories.as_view(), name='category'),
    path('product-detail/<slug>', ProductView.as_view(), name='product-detail'),
    path('reviews', reviews, name='reviews'),
]
