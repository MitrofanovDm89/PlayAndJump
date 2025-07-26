from django.core.management.base import BaseCommand
import os
import shutil
from django.conf import settings

class Command(BaseCommand):
    help = 'Copy images for Vermietung page from Backup to static files'

    def handle(self, *args, **options):
        self.stdout.write('Copying images for Vermietung page...')
        
        # Define image mappings
        image_mappings = {
            'rutsche.jpg': 'Rutsche.jpg',
            'event-betreuung.jpg': 'kinderschminken-Geburtstag-.jpg',
            'stromerzeuger.jpg': 'Stromerzeuger-scaled.jpg',
            'schalldaemmung.jpg': 'placeholder.png',  # Placeholder for now
            'zuckerwatte.jpg': 'Zuckerwatte-Rastatt-scaled.jpg',
            'kinderschminken.jpg': 'Wolf-Kinderschminken.jpg',
            'delphin.jpg': 'Delphin.jpg',
            'huepfburg-weiss.jpg': 'hupfburg-zirkus-super-3.jpg',  # White castle image
            'fussball-darts.jpg': 'Fussball-Darts-1-scaled.jpg',
        }
        
        # Source and destination directories
        backup_dir = os.path.join(settings.BASE_DIR, 'Backup', 'used_images')
        static_dir = os.path.join(settings.BASE_DIR, 'main', 'static', 'main', 'img')
        
        # Create static directory if it doesn't exist
        os.makedirs(static_dir, exist_ok=True)
        
        copied_count = 0
        for dest_name, source_name in image_mappings.items():
            source_path = os.path.join(backup_dir, source_name)
            dest_path = os.path.join(static_dir, dest_name)
            
            if os.path.exists(source_path):
                shutil.copy2(source_path, dest_path)
                self.stdout.write(f'✓ Copied {source_name} → {dest_name}')
                copied_count += 1
            else:
                self.stdout.write(f'⚠ Source file not found: {source_name}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully copied {copied_count} images!'))
        
        # List all images in static directory
        self.stdout.write('\nImages in static directory:')
        for file in os.listdir(static_dir):
            if file.endswith(('.jpg', '.jpeg', '.png')):
                self.stdout.write(f'• {file}') 