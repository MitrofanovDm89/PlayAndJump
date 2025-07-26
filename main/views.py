from django.shortcuts import render, get_object_or_404
from django.http import Http404
from catalog.models import Product
from .models import Page

def home(request):
    featured = Product.objects.filter(is_active=True)[:4]
    return render(request, 'main/home.html', {'featured': featured})

def kontakt(request):
    return render(request, 'pages/kontakt.html')

def agb(request):
    return render(request, 'pages/agb.html')

def impressum(request):
    return render(request, 'pages/impressum.html')

def datenschutz(request):
    return render(request, 'pages/datenschutz.html')

def ueber_uns(request):
    return render(request, 'pages/ueber_uns.html')
def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug, is_active=True)
    return render(request, 'main/page_detail.html', {'page': page})
