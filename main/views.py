from django.shortcuts import render
from django.conf import settings
from django.http import Http404
import json
import os
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


def _load_pages():
    pages_path = os.path.join(settings.BASE_DIR, 'Backup', 'pages.json')
    try:
        with open(pages_path, encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def page_detail(request, slug):
    pages = _load_pages()
    page = next((p for p in pages if p.get('slug') == slug), None)
    if not page:
        raise Http404('Page not found')
    return render(request, 'main/page_detail.html', {'page': page})
