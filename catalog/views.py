from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Availability
from cart.forms import CartAddProductForm
import json


def catalog_index(request):
    categories = Category.objects.all()
    return render(request, 'catalog/index.html', {'categories': categories})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, is_active=True)
    return render(request, 'catalog/category_detail.html', {
        'category': category,
        'products': products
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    form = CartAddProductForm()

    # Получаем все недоступные диапазоны дат
    unavail_ranges = Availability.objects.filter(
        product=product,
        is_available=False
    )

    # Собираем все отдельные недоступные даты
    unavailable_dates = []
    for entry in unavail_ranges:
        current = entry.start_date
        while current <= entry.end_date:
            unavailable_dates.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=1)

    return render(request, 'catalog/product_detail.html', {
        'product': product,
        'form': form,
        'unavailable_dates': json.dumps(unavailable_dates),  # мини-календарь
        'disabled_dates': json.dumps(unavailable_dates),     # flatpickr
    })
