from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)  # изображение категории

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="products/")
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Возвращает URL страницы товара по слагу
        return reverse('product_detail', args=[self.slug])


class Availability(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='availabilities')
    start_date = models.DateField()
    end_date = models.DateField()
    is_available = models.BooleanField(default=False)  # теперь по умолчанию товар недоступен

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        status = "verfügbar" if self.is_available else "nicht verfügbar"
        return f"{self.product.title} – {self.start_date} bis {self.end_date} – {status}"
