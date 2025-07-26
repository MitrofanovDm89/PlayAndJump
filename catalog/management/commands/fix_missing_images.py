from django.core.management.base import BaseCommand
from catalog.models import Product
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Fix missing images for products'

    def handle(self, *args, **options):
        self.stdout.write('Fixing missing images...')
        
        # Fix specific products with missing images using exact filenames
        fixes = {
            'huepfburg-dschungel': 'Dschungel-1.jpg'
        }
        
        for slug, image_name in fixes.items():
            try:
                product = Product.objects.get(slug=slug)
                image_path = os.path.join(settings.MEDIA_ROOT, 'products', image_name)
                
                if os.path.exists(image_path):
                    product.image = f'products/{image_name}'
                    product.save()
                    self.stdout.write(f'✓ Fixed image for {product.title}: {image_name}')
                else:
                    self.stdout.write(f'⚠ Image not found: {image_name}')
                    
            except Product.DoesNotExist:
                self.stdout.write(f'❌ Product not found: {slug}')
        
        # Show final status
        self.stdout.write('\nFinal status:')
        for product in Product.objects.all():
            image_status = '✓' if product.image else '❌'
            self.stdout.write(f'{image_status} {product.title}: {product.image or "No image"}')
        
        self.stdout.write(self.style.SUCCESS('Image fixes completed!')) 