from django.contrib import admin
from home import views
from django.urls import path, include

urlpatterns = [
    path('', views.product_list, name='home_view')
]