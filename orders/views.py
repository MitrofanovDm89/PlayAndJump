from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import datetime
from decimal import Decimal
import json

from .models import Order, OrderItem, Payment
from cart.models import Cart, CartItem
from cart.views import get_or_create_cart

def create_order_from_cart(request):
    """Создать заказ из корзины"""
    if request.method == 'POST':
        data = json.loads(request.body)
        
        cart = get_or_create_cart(request)
        if not cart.items.exists():
            return JsonResponse({'error': 'Cart is empty'}, status=400)
        
        # Create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            cart=cart,
            customer_name=data.get('customer_name'),
            customer_email=data.get('customer_email'),
            customer_phone=data.get('customer_phone', ''),
            customer_address=data.get('customer_address'),
            total_amount=cart.total_price,
            tax_amount=cart.total_price * 0.19,  # 19% VAT
            shipping_amount=data.get('shipping_amount', 0),
            notes=data.get('notes', '')
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                service=cart_item.service,
                quantity=cart_item.quantity,
                unit_price=cart_item.price,
                total_price=cart_item.total_price,
                start_date=cart_item.start_date,
                end_date=cart_item.end_date
            )
        
        # Send confirmation email
        send_order_confirmation_email(order)
        
        # Clear cart
        cart.items.all().delete()
        
        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'redirect_url': f'/orders/{order.id}/'
        })
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def order_detail(request, order_id):
    """Детали заказа"""
    order = get_object_or_404(Order, id=order_id)
    
    # Check if user has permission to view this order
    if request.user.is_authenticated:
        if order.user and order.user != request.user:
            messages.error(request, 'Sie haben keine Berechtigung, diesen Auftrag anzuzeigen.')
            return redirect('home')
    else:
        # For anonymous users, check by email
        if order.customer_email != request.session.get('order_email'):
            messages.error(request, 'Sie haben keine Berechtigung, diesen Auftrag anzuzeigen.')
            return redirect('home')
    
    return render(request, 'orders/order_detail.html', {
        'order': order
    })

def order_list(request):
    """Список заказов пользователя"""
    if not request.user.is_authenticated:
        messages.error(request, 'Bitte melden Sie sich an, um Ihre Bestellungen anzuzeigen.')
        return redirect('login')
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'orders/order_list.html', {
        'orders': orders
    })

def checkout(request):
    """Страница оформления заказа"""
    cart = get_or_create_cart(request)
    
    if not cart.items.exists():
        messages.warning(request, 'Ihr Warenkorb ist leer.')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['customer_name', 'customer_email', 'customer_address']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'error': f'{field} is required'}, status=400)
        
        # Create order
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            cart=cart,
            customer_name=data['customer_name'],
            customer_email=data['customer_email'],
            customer_phone=data.get('customer_phone', ''),
            customer_address=data['customer_address'],
            total_amount=cart.total_price,
            tax_amount=cart.total_price * 0.19,
            shipping_amount=data.get('shipping_amount', 0),
            notes=data.get('notes', '')
        )
        
        # Create order items
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                service=cart_item.service,
                quantity=cart_item.quantity,
                unit_price=cart_item.price,
                total_price=cart_item.total_price,
                start_date=cart_item.start_date,
                end_date=cart_item.end_date
            )
        
        # Store email in session for anonymous users
        if not request.user.is_authenticated:
            request.session['order_email'] = data['customer_email']
        
        # Send confirmation email
        send_order_confirmation_email(order)
        
        # Clear cart
        cart.items.all().delete()
        
        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'redirect_url': f'/orders/{order.id}/'
        })
    
    return render(request, 'orders/checkout.html', {
        'cart': cart
    })

def send_order_confirmation_email(order):
    """Отправить email подтверждения заказа"""
    subject = f'Bestellbestätigung - {order.order_number}'
    
    html_message = render_to_string('orders/email/order_confirmation.html', {
        'order': order
    })
    
    try:
        send_mail(
            subject=subject,
            message='',
            html_message=html_message,
            from_email='noreply@playandjump.de',
            recipient_list=[order.customer_email],
            fail_silently=False
        )
    except Exception as e:
        print(f"Error sending email: {e}")

def order_tracking(request, order_number):
    """Отслеживание заказа по номеру"""
    order = get_object_or_404(Order, order_number=order_number)
    
    return render(request, 'orders/order_tracking.html', {
        'order': order
    })

def quick_confirm_order(request):
    """Быстрое подтверждение заказа"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cart = get_or_create_cart(request)
            
            if not cart.items.exists():
                return JsonResponse({'success': False, 'error': 'Warenkorb ist leer'})
            
            # Создать заказ с данными по умолчанию
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                cart=cart,
                customer_name=request.user.get_full_name() if request.user.is_authenticated else 'Gast',
                customer_email=request.user.email if request.user.is_authenticated else '',
                customer_phone='',
                customer_address='',
                total_amount=cart.total_price,
                tax_amount=cart.total_price * Decimal('0.19'),
                shipping_amount=Decimal('0.00'),
                status='confirmed',
                payment_status='pending',
                payment_method=data.get('payment_method', 'invoice'),
                notes='Schnellbestellung'
            )
            
            # Создать элементы заказа
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    service=item.service,
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                    total_price=item.total_price,
                    start_date=item.start_date,
                    end_date=item.end_date
                )
            
            # Очистить корзину
            cart.delete()
            
            return JsonResponse({
                'success': True,
                'order_number': order.order_number,
                'redirect_url': f'/orders/{order.id}/'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Nur POST-Anfragen erlaubt'})

def request_quote(request):
    """Запрос коммерческого предложения"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Здесь можно добавить логику сохранения запроса в базу данных
            # или отправки email
            
            # Отправить email с запросом
            subject = 'Angebotsanfrage - Play & Jump'
            message = f"""
Neue Angebotsanfrage:

Firmenname: {data.get('company_name')}
Ansprechpartner: {data.get('contact_person')}
E-Mail: {data.get('email')}
Anzahl Artikel: {data.get('cart_items')}

Datum: {timezone.now().strftime('%d.%m.%Y %H:%M')}
            """
            
            # В реальном проекте здесь будет отправка email
            print(f"Quote request: {message}")
            
            return JsonResponse({'success': True})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Nur POST-Anfragen erlaubt'})
