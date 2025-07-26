from django.core.management.base import BaseCommand
from catalog.models import Product
import os
import shutil
from django.conf import settings


class Command(BaseCommand):
    help = 'Clear all products and their images'

    def handle(self, *args, **options):
        self.stdout.write('Clearing all products...')
        
        # Delete all products
        products_count = Product.objects.count()
        Product.objects.all().delete()
        self.stdout.write(f'Deleted {products_count} products')
        
        # Clear products images directory
        media_products_path = os.path.join(settings.MEDIA_ROOT, 'products')
        if os.path.exists(media_products_path):
            shutil.rmtree(media_products_path)
            self.stdout.write('Cleared products images directory')
        
        self.stdout.write(self.style.SUCCESS('All products cleared successfully!')) 