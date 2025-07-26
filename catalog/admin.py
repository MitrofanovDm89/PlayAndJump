from django.contrib import admin
from .models import Product, Category, Availability


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # автозаполнение


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'is_active', 'category')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'description')


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('product', 'start_date', 'end_date', 'is_available')
    list_filter = ('product', 'is_available')
    search_fields = ('product__title',)
    date_hierarchy = 'start_date'  # для удобной навигации по датам

