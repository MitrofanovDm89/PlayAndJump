from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from catalog.models import Product, Availability
from .cart import Cart
from .forms import CartAddProductForm


def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        start = cd['rental_start']
        end = cd['rental_end']

        # ❗ Проверка: не пересекается ли выбранный диапазон с занятыми
        unavailable_ranges = Availability.objects.filter(
            product=product,
            is_available=False
        )

        all_unavailable = set()
        for entry in unavailable_ranges:
            current = entry.start_date
            while current <= entry.end_date:
                all_unavailable.add(current)
                current += timedelta(days=1)

        # Проверка на конфликт дат
        current = start
        while current <= end:
            if current in all_unavailable:
                messages.error(request, f"❌ Das Produkt ist am {current} nicht verfügbar.")
                return redirect(product.get_absolute_url())
            current += timedelta(days=1)

        # ✅ Всё в порядке — добавляем в корзину
        cart = Cart(request)
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override'],
            rental_start=start,
            rental_end=end
        )
        messages.success(request, f"✅ Produkt von {start} bis {end} wurde in den Warenkorb gelegt.")
    else:
        messages.error(request, "❌ Ungültige Eingabe. Bitte überprüfe das Formular.")

    return redirect('cart:detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f"🗑️ {product.title} wurde aus dem Warenkorb entfernt.")
    return redirect('cart:detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})
