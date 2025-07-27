from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime
import json

from .models import Cart, CartItem
from catalog.models import Product, Service

def get_or_create_cart(request):
    """Получить или создать корзину для пользователя"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    return cart

def add_to_cart(request):
    """Добавить товар в корзину"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"📦 Получены данные: {data}")  # Отладочная информация
            
            item_type = data.get('item_type')
            item_id = data.get('item_id')
            quantity = int(data.get('quantity', 1))
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            
            cart = get_or_create_cart(request)
            
            # Валидация дат
            if start_date and end_date:
                from datetime import datetime
                try:
                    start = datetime.strptime(start_date, '%Y-%m-%d').date()
                    end = datetime.strptime(end_date, '%Y-%m-%d').date()
                    today = timezone.now().date()
                    
                    if start < today:
                        return JsonResponse({'error': 'Das Anfangsdatum kann nicht in der Vergangenheit liegen.'}, status=400)
                    
                    if end < start:
                        return JsonResponse({'error': 'Das Enddatum muss nach dem Anfangsdatum liegen.'}, status=400)
                        
                except ValueError:
                    return JsonResponse({'error': 'Ungültiges Datumsformat.'}, status=400)
            
            if item_type == 'product':
                item = get_object_or_404(Product, id=item_id, is_active=True)
                price = item.price or 0
            elif item_type == 'service':
                item = get_object_or_404(Service, id=item_id, is_active=True)
                price = item.price
            else:
                return JsonResponse({'error': 'Invalid item type'}, status=400)
            
            # Проверяем, есть ли уже такой товар в корзине
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                item_type=item_type,
                product=item if item_type == 'product' else None,
                service=item if item_type == 'service' else None,
                defaults={
                    'quantity': quantity,
                    'price': price,
                    'start_date': start_date,
                    'end_date': end_date
                }
            )
            
            if not created:
                cart_item.quantity += quantity
                # Обновляем даты, если они предоставлены
                if start_date:
                    cart_item.start_date = start_date
                if end_date:
                    cart_item.end_date = end_date
                cart_item.save()
            
            return JsonResponse({
                'success': True,
                'cart_count': cart.item_count,
                'cart_total': float(cart.total_price)
            })
        except Exception as e:
            print(f"❌ Ошибка в add_to_cart: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def add_service_to_cart(request):
    """Добавить дополнительную услугу в корзину"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            service_type = data.get('service_type')
            price = data.get('price', 0)
            message = data.get('message', '')
            
            cart = get_or_create_cart(request)
            
            # Создать специальный сервис в корзине
            cart_item = CartItem.objects.create(
                cart=cart,
                item_type='service',
                service=None,  # Это дополнительная услуга
                quantity=1,
                price=price,
                notes=f"{service_type}: {message}".strip()
            )
            
            return JsonResponse({
                'success': True,
                'cart_count': cart.item_count,
                'cart_total': float(cart.total_price)
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def remove_from_cart(request, item_id):
    """Удалить товар из корзины"""
    cart = get_or_create_cart(request)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    
    return JsonResponse({
        'success': True,
        'cart_count': cart.item_count,
        'cart_total': float(cart.total_price)
    })

def update_cart_item(request, item_id):
    """Обновить количество товара в корзине"""
    if request.method == 'POST':
        data = json.loads(request.body)
        quantity = int(data.get('quantity', 1))
        
        cart = get_or_create_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count,
            'cart_total': float(cart.total_price),
            'item_total': float(cart_item.total_price) if quantity > 0 else 0
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def cart_detail(request):
    """Страница корзины"""
    cart = get_or_create_cart(request)
    
    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'cart_items': cart.items.all()
    })

def clear_cart(request):
    """Очистить корзину"""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    
    return JsonResponse({
        'success': True,
        'cart_count': 0,
        'cart_total': 0
    })

def get_cart_count(request):
    """Получить количество товаров в корзине для AJAX"""
    cart = get_or_create_cart(request)
    return JsonResponse({
        'cart_count': cart.item_count,
        'cart_total': float(cart.total_price)
    })
