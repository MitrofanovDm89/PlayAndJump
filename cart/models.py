from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product, Service
from django.utils import timezone

class Cart(models.Model):
    """Модель корзины пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart {self.id} - {self.user or self.session_key}"
    
    @property
    def total_price(self):
        """Общая стоимость корзины"""
        return sum(item.total_price for item in self.items.all())
    
    @property
    def item_count(self):
        """Количество товаров в корзине"""
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    """Товар в корзине"""
    ITEM_TYPE_CHOICES = [
        ('product', 'Produkt'),
        ('service', 'Service'),
    ]
    
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=10, choices=ITEM_TYPE_CHOICES)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    start_date = models.DateField(null=True, blank=True)  # для аренды
    end_date = models.DateField(null=True, blank=True)    # для аренды
    price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)  # для дополнительных заметок
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['cart', 'item_type', 'product', 'service']
    
    def __str__(self):
        if self.product:
            return f"{self.product.title} x{self.quantity}"
        elif self.service:
            return f"{self.service.title} x{self.quantity}"
        return f"Item {self.id}"
    
    @property
    def total_price(self):
        """Общая стоимость позиции"""
        if self.start_date and self.end_date:
            days = (self.end_date - self.start_date).days + 1
            return self.price * days * self.quantity
        return self.price * self.quantity
    
    @property
    def item_name(self):
        """Название товара/услуги"""
        if self.product:
            return self.product.title
        elif self.service:
            return self.service.title
        return "Unbekanntes Item"
