from django.core.management.base import BaseCommand
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from catalog.models import Category, Product
import os
import shutil
from django.conf import settings


class Command(BaseCommand):
    help = 'Import products from Backup images'

    def handle(self, *args, **options):
        self.stdout.write('Starting product import...')
        
        # Create categories
        categories = {
            'huepfburgen': {
                'name': 'Hüpfburgen',
                'description': 'Sichere und hochwertige Hüpfburgen für alle Altersgruppen'
            },
            'spielgeraete': {
                'name': 'Spielgeräte',
                'description': 'Verschiedene Spielgeräte für Unterhaltung und Spaß'
            },
            'unterhaltung': {
                'name': 'Unterhaltung',
                'description': 'Unterhaltungsangebote für Events und Feiern'
            },
            'lebensmittel': {
                'name': 'Lebensmittel',
                'description': 'Popcorn-Maschinen und andere Lebensmittelgeräte'
            }
        }
        
        # Create categories
        created_categories = {}
        for slug, data in categories.items():
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': data['name'],
                    'description': data['description']
                }
            )
            created_categories[slug] = category
            if created:
                self.stdout.write(f'Created category: {category.name}')
        
        # Product data based on images from Backup
        products_data = [
            {
                'title': 'Hüpfburg "Circus"',
                'slug': 'huepfburg-circus',
                'description': 'Große, sichere Hüpfburg im Zirkus-Design. Perfekt für Kindergeburtstage und Events. Maximale Belastung: 500kg.',
                'price': 150.00,
                'category': 'huepfburgen',
                'image_file': 'hupfburg-zirkus-super-2.jpg'
            },
            {
                'title': 'Hüpfburg "Dschungel"',
                'slug': 'huepfburg-dschungel',
                'description': 'Spannende Dschungel-Hüpfburg mit wilden Tieren. Ideal für Abenteuer-Theme Events.',
                'price': 120.00,
                'category': 'huepfburgen',
                'image_file': 'Dschungel-1.jpg'
            },
            {
                'title': 'Hüpfburg "Polizei"',
                'slug': 'huepfburg-polizei',
                'description': 'Polizei-Theme Hüpfburg für kleine Helden. Mit Polizei-Design und Sicherheitsausrüstung.',
                'price': 130.00,
                'category': 'huepfburgen',
                'image_file': 'Play-Jump-Polizei-1-scaled.jpg'
            },
            {
                'title': 'Darts XXL',
                'slug': 'darts-xxl',
                'description': 'Großes Dart-Spiel für Erwachsene und Jugendliche. Professionelle Ausrüstung.',
                'price': 80.00,
                'category': 'spielgeraete',
                'image_file': 'Dart-XXL1.jpg'
            },
            {
                'title': 'Fussball-Billiard',
                'slug': 'fussball-billiard',
                'description': 'Kombination aus Fußball und Billard. Einzigartiges Spielgerät für Events.',
                'price': 90.00,
                'category': 'spielgeraete',
                'image_file': 'Fussball-Billiard-1.jpeg'
            },
            {
                'title': 'Shooting Combo',
                'slug': 'shooting-combo',
                'description': 'Schießstand-Kombination mit verschiedenen Spielmodi. Sicher und unterhaltsam.',
                'price': 100.00,
                'category': 'spielgeraete',
                'image_file': 'Shooting-Combo.jpg'
            },
            {
                'title': 'XXL Schach',
                'slug': 'xxl-schach',
                'description': 'Riesiges Schachspiel für draußen. Perfekt für Parks und Events.',
                'price': 70.00,
                'category': 'spielgeraete',
                'image_file': 'XXL-Schach-Play-Jump-1-scaled.jpg'
            },
            {
                'title': 'Popcorn-Maschine',
                'slug': 'popcorn-maschine',
                'description': 'Professionelle Popcorn-Maschine für Events. Frisches Popcorn für alle Gäste.',
                'price': 60.00,
                'category': 'lebensmittel',
                'image_file': 'POpcornmaschine-Rastatt-1.jpg'
            },
            {
                'title': 'Zuckerwatte-Maschine',
                'slug': 'zuckerwatte-maschine',
                'description': 'Zuckerwatte-Maschine für süße Überraschungen. Ideal für Kinderfeste.',
                'price': 50.00,
                'category': 'lebensmittel',
                'image_file': 'ZUCKERWATTEMASCHINE_.jpg'
            },
            {
                'title': 'Kinderschminken',
                'slug': 'kinderschminken',
                'description': 'Professioneller Kinderschmink-Service. Verschiedene Motive und Designs.',
                'price': 100.00,
                'category': 'unterhaltung',
                'image_file': 'kinderschminken-Geburtstag-.jpg'
            },
            {
                'title': 'Stromerzeuger',
                'slug': 'stromerzeuger',
                'description': 'Professioneller Stromerzeuger für Events. Zuverlässige Stromversorgung.',
                'price': 80.00,
                'category': 'unterhaltung',
                'image_file': 'Stromerzeuger-1-scaled.jpg'
            },
            {
                'title': 'Party-Dekoration',
                'slug': 'party-dekoration',
                'description': 'Vollständige Party-Dekoration für verschiedene Anlässe. Farben und Motive wählbar.',
                'price': 40.00,
                'category': 'unterhaltung',
                'image_file': 'Party-1.jpg'
            }
        ]
        
        # Import products
        backup_images_path = os.path.join(settings.BASE_DIR, 'Backup', 'used_images')
        media_products_path = os.path.join(settings.MEDIA_ROOT, 'products')
        
        # Create products directory if it doesn't exist
        os.makedirs(media_products_path, exist_ok=True)
        
        for product_data in products_data:
            # Check if product already exists
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={
                    'title': product_data['title'],
                    'description': product_data['description'],
                    'price': product_data['price'],
                    'category': created_categories[product_data['category']],
                    'is_active': True
                }
            )
            
            if created:
                # Copy image file
                source_image = os.path.join(backup_images_path, product_data['image_file'])
                if os.path.exists(source_image):
                    dest_image = os.path.join(media_products_path, product_data['image_file'])
                    shutil.copy2(source_image, dest_image)
                    
                    # Update product with image
                    product.image = f"products/{product_data['image_file']}"
                    product.save()
                    
                    self.stdout.write(f'Created product: {product.title} with image')
                else:
                    self.stdout.write(f'Warning: Image not found for {product.title}: {product_data["image_file"]}')
            else:
                self.stdout.write(f'Product already exists: {product.title}')
        
        self.stdout.write(self.style.SUCCESS('Product import completed successfully!')) 