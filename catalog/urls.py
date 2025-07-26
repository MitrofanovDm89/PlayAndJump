from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_index, name='catalog_index'),  # ← вот эта строка
    path('<slug:slug>/', views.category_detail, name='category_detail'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]
