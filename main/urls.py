from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('kontakt/', views.kontakt, name='kontakt'),
    path('agb/', views.agb, name='agb'),
    path('impressum/', views.impressum, name='impressum'),
    path('datenschutz/', views.datenschutz, name='datenschutz'),
    path('ueber-uns/', views.ueber_uns, name='ueber_uns'),
]
