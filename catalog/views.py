from datetime import timedelta
from django.shortcuts import render, get_object_or_404
from .models import Product, Category, Availability
from cart.forms import CartAddProductForm
import json


def catalog_index(request):
    base_categories = [
        {'slug': 'huepfburgen', 'name': 'H\u00fcpfburgen', 'url_name': 'huepfburgen'},
        {'slug': 'gesellschaftsspiele', 'name': 'Gesellschaftsspiele', 'url_name': 'gesellschaftsspiele'},
        {'slug': 'funfood', 'name': 'Fun Food', 'url_name': 'funfood'},
    ]

    existing = {c.slug: c for c in Category.objects.filter(slug__in=[b['slug'] for b in base_categories])}
    categories = []
    for item in base_categories:
        cat = existing.get(item['slug'])
        name = cat.name if cat else item['name']
        if cat and cat.image:
            image_url = cat.image.url
        else:
            placeholder_text = name.replace(' ', '+')
            image_url = f'https://via.placeholder.com/400x250?text={placeholder_text}'
        categories.append({'name': name, 'image_url': image_url, 'url_name': item['url_name']})

    return render(request, 'catalog/index.html', {'categories': categories})


def huepfburgen(request):
    return render(request, 'catalog/huepfburgen.html')


def gesellschaftsspiele(request):
    return render(request, 'catalog/gesellschaftsspiele.html')


def funfood(request):
    return render(request, 'catalog/funfood.html')


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
