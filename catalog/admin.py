from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db.models import Sum, Count
from .models import Product, Category, Availability, Booking


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'product_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    ordering = ('name',)
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Количество товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'is_active', 'image_preview', 'booking_count')
    list_filter = ('is_active', 'category')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description')
    readonly_fields = ('image_preview', 'booking_count')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'category', 'description', 'image')
        }),
        ('Цена и статус', {
            'fields': ('price', 'is_active')
        }),
        ('Статистика', {
            'fields': ('booking_count', 'image_preview'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 50px; object-fit: cover;" />',
                obj.image.url
            )
        return "Нет изображения"
    image_preview.short_description = 'Изображение'
    
    def booking_count(self, obj):
        count = obj.bookings.count()
        if count > 0:
            url = reverse('admin:catalog_booking_changelist') + f'?product__id__exact={obj.id}'
            return format_html('<a href="{}">{} бронирований</a>', url, count)
        return "0 бронирований"
    booking_count.short_description = 'Бронирования'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'product', 'start_date', 'end_date', 'total_price', 'status', 'duration_days')
    list_filter = ('status', 'product', 'start_date', 'created_at')
    search_fields = ('customer_name', 'customer_email', 'product__title')
    readonly_fields = ('duration_days', 'created_at', 'updated_at')
    date_hierarchy = 'start_date'
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Детали бронирования', {
            'fields': ('product', 'start_date', 'end_date', 'total_price', 'status')
        }),
        ('Дополнительно', {
            'fields': ('notes', 'duration_days'),
            'classes': ('collapse',)
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def duration_days(self, obj):
        return obj.duration_days
    duration_days.short_description = 'Дней'
    
    actions = ['mark_confirmed', 'mark_cancelled', 'mark_completed']
    
    def mark_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} бронирований подтверждено.')
    mark_confirmed.short_description = "Подтвердить выбранные бронирования"
    
    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} бронирований отменено.')
    mark_cancelled.short_description = "Отменить выбранные бронирования"
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} бронирований завершено.')
    mark_completed.short_description = "Завершить выбранные бронирования"


@admin.register(Availability)
class AvailabilityAdmin(admin.ModelAdmin):
    list_display = ('product', 'start_date', 'end_date', 'is_available', 'duration_days')
    list_filter = ('product', 'is_available', 'start_date')
    search_fields = ('product__title',)
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    
    def duration_days(self, obj):
        return (obj.end_date - obj.start_date).days + 1
    duration_days.short_description = 'Дней'


# Кастомная админка для дашборда
class PlayAndJumpAdminSite(admin.AdminSite):
    site_header = "Play & Jump - Администрирование"
    site_title = "Play & Jump Admin"
    index_title = "Панель управления"
    
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        
        # Добавляем статистику
        stats = {
            'total_products': Product.objects.count(),
            'active_products': Product.objects.filter(is_active=True).count(),
            'total_bookings': Booking.objects.count(),
            'pending_bookings': Booking.objects.filter(status='pending').count(),
            'confirmed_bookings': Booking.objects.filter(status='confirmed').count(),
            'total_revenue': Booking.objects.filter(status='confirmed').aggregate(Sum('total_price'))['total_price__sum'] or 0,
        }
        
        # Добавляем статистику в контекст
        self.stats = stats
        
        return app_list


# Регистрируем кастомную админку
admin_site = PlayAndJumpAdminSite(name='playandjump_admin')

# Регистрируем модели в кастомной админке
admin_site.register(Category, CategoryAdmin)
admin_site.register(Product, ProductAdmin)
admin_site.register(Booking, BookingAdmin)
admin_site.register(Availability, AvailabilityAdmin)

