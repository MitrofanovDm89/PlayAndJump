from django.core.management.base import BaseCommand
from django.conf import settings
import os
import shutil

class Command(BaseCommand):
    help = 'Fix image for Gebläse Schalldämmung'

    def handle(self, *args, **options):
        self.stdout.write('Fixing image for Gebläse Schalldämmung...')
        
        try:
            # Source and destination paths
            source_path = os.path.join(settings.BASE_DIR, 'Backup', 'used_images', 'Stromerzeuger-1-scaled.jpg')
            dest_path = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'img', 'schalldaemmung.jpg')
            
            # Copy the image
            if os.path.exists(source_path):
                shutil.copy2(source_path, dest_path)
                self.stdout.write(f'✅ Fixed image for Gebläse Schalldämmung: {dest_path}')
                self.stdout.write(f'📏 File size: {os.path.getsize(dest_path) / 1024:.1f} KB')
            else:
                self.stdout.write(f'❌ Source image not found: {source_path}')
                
        except Exception as e:
            self.stdout.write(f'❌ Error: {e}') 