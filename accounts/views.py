from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
import json

from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, UserAddressForm
from .models import UserProfile, UserAddress
from orders.models import Order

def register_view(request):
    """Страница регистрации"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrierung erfolgreich! Willkommen bei Play & Jump.')
            return redirect('home')
        else:
            messages.error(request, 'Bitte korrigieren Sie die Fehler unten.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {
        'form': form
    })

def login_view(request):
    """Страница входа"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Willkommen zurück, {user.first_name or user.username}!')
                return redirect('home')
        else:
            messages.error(request, 'Ungültige Anmeldedaten.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {
        'form': form
    })

def logout_view(request):
    """Выход из системы"""
    logout(request)
    messages.success(request, 'Sie wurden erfolgreich abgemeldet.')
    return redirect('home')

@login_required
def profile_view(request):
    """Страница профиля пользователя"""
    user = request.user
    
    # Получить статистику заказов
    orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    total_orders = Order.objects.filter(user=user).count()
    total_spent = sum(order.grand_total for order in Order.objects.filter(user=user))
    
    # Получить адреса
    addresses = UserAddress.objects.filter(user=user)
    
    context = {
        'user': user,
        'profile': user.profile,
        'orders': orders,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'addresses': addresses,
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile_view(request):
    """Редактирование профиля"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil erfolgreich aktualisiert.')
            return redirect('accounts:profile')
        else:
            messages.error(request, 'Bitte korrigieren Sie die Fehler unten.')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'accounts/edit_profile.html', {
        'form': form
    })

@login_required
def address_list_view(request):
    """Список адресов пользователя"""
    addresses = UserAddress.objects.filter(user=request.user)
    
    return render(request, 'accounts/address_list.html', {
        'addresses': addresses
    })

@login_required
def add_address_view(request):
    """Добавление нового адреса"""
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Adresse erfolgreich hinzugefügt.')
            return redirect('accounts:address_list')
        else:
            messages.error(request, 'Bitte korrigieren Sie die Fehler unten.')
    else:
        form = UserAddressForm()
    
    return render(request, 'accounts/add_address.html', {
        'form': form
    })

@login_required
def edit_address_view(request, address_id):
    """Редактирование адреса"""
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)
    
    if request.method == 'POST':
        form = UserAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Adresse erfolgreich aktualisiert.')
            return redirect('accounts:address_list')
        else:
            messages.error(request, 'Bitte korrigieren Sie die Fehler unten.')
    else:
        form = UserAddressForm(instance=address)
    
    return render(request, 'accounts/edit_address.html', {
        'form': form,
        'address': address
    })

@login_required
@require_POST
def delete_address_view(request, address_id):
    """Удаление адреса"""
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)
    address.delete()
    messages.success(request, 'Adresse erfolgreich gelöscht.')
    return redirect('accounts:address_list')

@login_required
def order_history_view(request):
    """История заказов пользователя"""
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'accounts/order_history.html', {
        'page_obj': page_obj
    })

@login_required
def dashboard_view(request):
    """Панель управления пользователя"""
    user = request.user
    
    # Статистика
    total_orders = Order.objects.filter(user=user).count()
    total_spent = sum(order.grand_total for order in Order.objects.filter(user=user))
    recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    addresses_count = UserAddress.objects.filter(user=user).count()
    
    # Обновить статистику в профиле
    profile = user.profile
    profile.total_orders = total_orders
    profile.total_spent = total_spent
    profile.save()
    
    context = {
        'user': user,
        'profile': profile,
        'total_orders': total_orders,
        'total_spent': total_spent,
        'recent_orders': recent_orders,
        'addresses_count': addresses_count,
    }
    
    return render(request, 'accounts/dashboard.html', context)
