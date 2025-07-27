from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('create/', views.create_order_from_cart, name='create_order'),
    # path('quick-confirm/', views.quick_confirm_order, name='quick_confirm'),
    path('request-quote/', views.request_quote, name='request_quote'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('list/', views.order_list, name='order_list'),
    path('tracking/<str:order_number>/', views.order_tracking, name='order_tracking'),
] 