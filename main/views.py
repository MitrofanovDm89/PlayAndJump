from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from catalog.models import Product

def home(request):
    featured = Product.objects.filter(is_active=True).order_by('?')[:4]  # Random 4 products
    return render(request, 'main/home.html', {'featured': featured})

def kontakt(request):
    return render(request, 'main/kontakt.html')

def agb(request):
    return render(request, 'main/agb.html')

def impressum(request):
    return render(request, 'main/impressum.html')

def datenschutz(request):
    return render(request, 'main/datenschutz.html')

def ueber_uns(request):
    return render(request, 'main/ueber_uns.html')

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
    products_list = Product.objects.filter(is_active=True).order_by('title')
    
    # Pagination
    paginator = Paginator(products_list, 12)  # 12 products per page
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)
    
    return render(request, 'main/katalog.html', {'products': products})

def product_detail(request, slug):
    """Страница деталей товара"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    
    # Get related products from same category
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]
    
    return render(request, 'main/product_detail.html', {
        'product': product,
        'related_products': related_products
    })
