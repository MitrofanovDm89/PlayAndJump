from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from catalog.models import Product, Booking, Category
from datetime import date, timedelta
import json

def home(request):
    """Главная страница - визитка компании"""
    return render(request, 'main/home.html')

def kontakt(request):
    return render(request, 'main/kontakt.html')

def agb(request):
    return render(request, 'main/agb.html')

def impressum(request):
    return render(request, 'main/impressum.html')

def datenschutz(request):
    return render(request, 'main/datenschutz.html')

def vermietung(request):
    """Страница аренды оборудования"""
    return render(request, 'main/vermietung.html')

def neuigkeiten(request):
    """Страница новостей"""
    return render(request, 'main/neuigkeiten.html')

def cart(request):
    """Страница корзины"""
    return render(request, 'main/cart.html')

def katalog(request):
    """Страница каталога"""
    # Get all categories for filter
    categories = Category.objects.all().order_by('name')
    
    # Get filter parameters
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search')
    
    # Start with all active products
    products_list = Product.objects.filter(is_active=True)
    
    # Apply category filter
    if category_filter:
        products_list = products_list.filter(category__slug=category_filter)
    
    # Apply search filter
    if search_query:
        products_list = products_list.filter(title__icontains=search_query)
    
    # Order by title
    products_list = products_list.order_by('title')
    
    # Pagination
    paginator = Paginator(products_list, 12)  # 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    return render(request, 'main/katalog.html', {
        'products': products,
        'categories': categories,
        'current_category': category_filter,
        'search_query': search_query
    })

def product_detail(request, slug):
    """Страница деталей товара"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Get related products from same category
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    # Get booked dates for the next 3 months
    today = date.today()
    end_date = today + timedelta(days=90)
    
    # Get confirmed and pending bookings
    bookings = Booking.objects.filter(
        product=product,
        start_date__gte=today,
        end_date__lte=end_date,
        status__in=['confirmed', 'pending']
    ).order_by('start_date')
    
    # Create list of booked dates for JavaScript
    booked_dates = []
    for booking in bookings:
        current_date = booking.start_date
        while current_date <= booking.end_date:
            booked_dates.append(current_date.strftime('%Y-%m-%d'))
            current_date += timedelta(days=1)
    
    return render(request, 'main/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'booked_dates': json.dumps(booked_dates),
        'bookings': bookings
    })
