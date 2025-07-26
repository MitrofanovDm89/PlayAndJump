from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_index, name='catalog_index'),  # ← вот эта строка
    # Маршрут для страницы товара должен располагаться выше,
    # иначе его "перехватит" маршрут категории
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('<slug:slug>/', views.category_detail, name='category_detail'),
]
