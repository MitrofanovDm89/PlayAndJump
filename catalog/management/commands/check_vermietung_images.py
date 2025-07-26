from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Check all images used on Vermietung page'

    def handle(self, *args, **options):
        self.stdout.write('Checking images for Vermietung page...')
        
        # List of images used on Vermietung page
        vermietung_images = [
            'main/img/rutsche.jpg',
            'main/img/event-betreuung.jpg', 
            'main/img/stromerzeuger.jpg',
            'main/img/schalldaemmung.jpg',
            'main/img/zuckerwatte.jpg',
            'main/img/kinderschminken.jpg',
            'main/img/delphin.jpg',
            'main/img/huepfburg-weiss.jpg',
            'main/img/fussball-darts.jpg'
        ]
        
        static_dir = os.path.join(settings.BASE_DIR, 'main', 'static')
        
        for image_path in vermietung_images:
            full_path = os.path.join(static_dir, image_path)
            
            if os.path.exists(full_path):
                file_size = os.path.getsize(full_path)
                size_kb = file_size / 1024
                
                if size_kb < 10:
                    status = "❌"
                    note = " (VERY SMALL - likely placeholder)"
                elif size_kb < 50:
                    status = "⚠️"
                    note = " (small)"
                else:
                    status = "✅"
                    note = ""
                
                self.stdout.write(f'{status} {image_path}: {size_kb:.1f} KB{note}')
            else:
                self.stdout.write(f'❌ {image_path}: FILE NOT FOUND')
        
        self.stdout.write('\n📊 Summary:')
        self.stdout.write('✅ = Good quality image (>50KB)')
        self.stdout.write('⚠️ = Small image (10-50KB)') 
        self.stdout.write('❌ = Very small or missing image (<10KB)') 