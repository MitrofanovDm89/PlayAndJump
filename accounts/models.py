from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    """Расширенный профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Дополнительная информация
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    
    # Настройки
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    
    # Статистика
    total_orders = models.PositiveIntegerField(default=0)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Даты
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Автоматически создавать профиль при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохранять профиль при изменении пользователя"""
    instance.profile.save()

class UserAddress(models.Model):
    """Адреса пользователя"""
    ADDRESS_TYPES = [
        ('billing', 'Rechnungsadresse'),
        ('shipping', 'Lieferadresse'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=20, choices=ADDRESS_TYPES)
    is_default = models.BooleanField(default=False)
    
    # Адрес
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    company = models.CharField(max_length=200, blank=True, null=True)
    street = models.CharField(max_length=200)
    house_number = models.CharField(max_length=10)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100, default='Deutschland')
    
    # Дополнительно
    phone = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.get_address_type_display()} - {self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        # Если этот адрес становится адресом по умолчанию, сбросить другие
        if self.is_default:
            UserAddress.objects.filter(
                user=self.user, 
                address_type=self.address_type
            ).exclude(pk=self.pk).update(is_default=False)
        super().save(*args, **kwargs)
