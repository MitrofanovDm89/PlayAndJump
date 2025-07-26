from django.shortcuts import render
from catalog.models import Product

def home(request):
    featured = Product.objects.filter(is_active=True)[:4]
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
    products = Product.objects.filter(is_active=True)
    return render(request, 'main/katalog.html', {'products': products})
