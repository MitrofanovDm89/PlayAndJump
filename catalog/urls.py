from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_index, name='catalog_index'),
    path('huepfburg/', views.huepfburg, name='huepfburg'),
    path('gesellschaftsspiele/', views.gesellschaftsspiele, name='gesellschaftsspiele'),
    path('funfood/', views.funfood, name='funfood'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:slug>/', views.category_detail, name='category_detail'),
]
