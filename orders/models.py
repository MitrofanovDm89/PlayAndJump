from django.db import models
from django.contrib.auth.models import User
from cart.models import Cart
from catalog.models import Product, Service
from django.utils import timezone

class Order(models.Model):
    """Модель заказа"""
    STATUS_CHOICES = [
        ('pending', 'Ausstehend'),
        ('confirmed', 'Bestätigt'),
        ('processing', 'In Bearbeitung'),
        ('shipped', 'Versendet'),
        ('delivered', 'Geliefert'),
        ('cancelled', 'Storniert'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Ausstehend'),
        ('paid', 'Bezahlt'),
        ('failed', 'Fehlgeschlagen'),
        ('refunded', 'Erstattet'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    
    # Customer information
    customer_name = models.CharField(max_length=200)
    customer_email = models.EmailField()
    customer_phone = models.CharField(max_length=20, blank=True)
    customer_address = models.TextField()
    
    # Order details
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    # Notes
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Order {self.order_number} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number
            last_order = Order.objects.order_by('-id').first()
            if last_order:
                last_number = int(last_order.order_number[3:])  # Remove 'ORD' prefix
                self.order_number = f"ORD{last_number + 1:06d}"
            else:
                self.order_number = "ORD000001"
        super().save(*args, **kwargs)
    
    @property
    def grand_total(self):
        """Общая сумма с налогами и доставкой"""
        return self.total_amount + self.tax_amount + self.shipping_amount

class OrderItem(models.Model):
    """Товар в заказе"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Rental dates
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        item_name = self.product.title if self.product else self.service.title
        return f"{item_name} x{self.quantity} - {self.order.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.total_price:
            if self.start_date and self.end_date:
                days = (self.end_date - self.start_date).days + 1
                self.total_price = self.unit_price * days * self.quantity
            else:
                self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)

class Payment(models.Model):
    """Модель платежа"""
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Banküberweisung'),
        ('paypal', 'PayPal'),
        ('credit_card', 'Kreditkarte'),
        ('cash', 'Bargeld'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    transaction_id = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=Order.PAYMENT_STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Payment {self.id} - {self.order.order_number} - {self.amount}€"
