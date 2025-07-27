from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Аутентификация
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Профиль
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Адреса
    path('addresses/', views.address_list_view, name='address_list'),
    path('addresses/add/', views.add_address_view, name='add_address'),
    path('addresses/<int:address_id>/edit/', views.edit_address_view, name='edit_address'),
    path('addresses/<int:address_id>/delete/', views.delete_address_view, name='delete_address'),
    
    # Заказы
    path('orders/', views.order_history_view, name='order_history'),
] 