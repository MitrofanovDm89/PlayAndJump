from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('agb/', views.agb, name='agb'),
    path('impressum/', views.impressum, name='impressum'),
    path('datenschutz/', views.datenschutz, name='datenschutz'),
    path('vermietung/', views.vermietung, name='vermietung'),
    path('neuigkeiten/', views.neuigkeiten, name='neuigkeiten'),
    path('cart/', views.cart, name='cart'),
    path('katalog/', views.katalog, name='katalog'),
    path('produkt/<slug:slug>/', views.product_detail, name='product_detail'),
]
