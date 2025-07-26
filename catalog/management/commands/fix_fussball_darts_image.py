from django.core.management.base import BaseCommand
from catalog.models import Product
from django.conf import settings
import os
import shutil

class Command(BaseCommand):
    help = 'Fix image for Fußball Darts product'

    def handle(self, *args, **options):
        self.stdout.write('Fixing image for Fußball Darts...')
        
        try:
            product = Product.objects.get(slug='fussball-darts')
            
            # Source and destination paths
            source_path = os.path.join(settings.BASE_DIR, 'Backup', 'used_images', 'Fussball-Darts-1-scaled.jpg')
            dest_path = os.path.join(settings.MEDIA_ROOT, 'products', 'Fussball-Darts-1-scaled.jpg')
            
            # Create products directory if it doesn't exist
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            
            # Copy the image
            if os.path.exists(source_path):
                shutil.copy2(source_path, dest_path)
                product.image = 'products/Fussball-Darts-1-scaled.jpg'
                product.save()
                self.stdout.write(f'✅ Fixed image for {product.title}: {product.image}')
            else:
                self.stdout.write(f'❌ Source image not found: {source_path}')
                
        except Product.DoesNotExist:
            self.stdout.write('❌ Product "fussball-darts" not found')
        except Exception as e:
            self.stdout.write(f'❌ Error: {e}') 