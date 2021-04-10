from django.contrib import admin
from home import views
from django.urls import path, include, re_path

urlpatterns = [
    path('', views.product_list, name='home_view'),
    re_path(r'^brand/(?P<brand_slug>[-\w]+)/$', views.product_list, name='product_list_by_brand'),
    re_path(r'^category/(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
    re_path(r'^subcategory/(?P<subcategory_slug>[-\w]+)/$', views.product_list, name='product_list_by_subcategory'),
    re_path(r'^product/(?P<id>[-\w]+)/$', views.product_detail, name='product_detail'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_page, name='logout_page'),
    path('register/', views.register_page, name='register_page'),
    re_path(r'^account/(?P<username>[-\w]+)/$', views.account_page, name='account_page'),
]