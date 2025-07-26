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
        
        # Create categories based on the old site structure
        categories = {
            'huepfburgen': {
                'name': 'Hüpfburg',
                'description': 'Sichere und hochwertige Hüpfburgen für alle Altersgruppen'
            },
            'gesellschaftsspiele': {
                'name': 'Gesellschaftsspiele',
                'description': 'Verschiedene Gesellschaftsspiele für Unterhaltung und Spaß'
            },
            'fun-food': {
                'name': 'Fun Food',
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
        
        # Product data based on the old site list
        products_data = [
            # Hüpfburgen Category
            {
                'title': 'Hüpfburg',
                'slug': 'huepfburg',
                'description': 'Klassische Hüpfburg für alle Altersgruppen. Sicher und stabil.',
                'price': 120.00,
                'category': 'huepfburgen',
                'image_file': 'hupfburg-zirkus-super-2.jpg'  # Placeholder image
            },
            {
                'title': 'Hüpfburg Zirkus',
                'slug': 'huepfburg-zirkus',
                'description': 'Große, sichere Hüpfburg im Zirkus-Design. Perfekt für Kindergeburtstage und Events.',
                'price': 150.00,
                'category': 'huepfburgen',
                'image_file': 'hupfburg-zirkus-super-2.jpg'
            },
            {
                'title': 'Hüpfburg Dschungel',
                'slug': 'huepfburg-dschungel',
                'description': 'Spannende Dschungel-Hüpfburg mit wilden Tieren. Ideal für Abenteuer-Theme Events.',
                'price': 130.00,
                'category': 'huepfburgen',
                'image_file': 'Dschungel-1.jpg'
            },
            {
                'title': 'Hüpfburg weiß',
                'slug': 'huepfburg-weiss',
                'description': 'Elegante weiße Hüpfburg für besondere Anlässe. Neutrales Design.',
                'price': 110.00,
                'category': 'huepfburgen',
                'image_file': 'hupfburg-zirkus-super-2.jpg'  # Placeholder
            },
            {
                'title': 'Hüpfburg Polizei',
                'slug': 'huepfburg-polizei',
                'description': 'Polizei-Theme Hüpfburg für kleine Helden. Mit Polizei-Design und Sicherheitsausrüstung.',
                'price': 130.00,
                'category': 'huepfburgen',
                'image_file': 'Play-Jump-Polizei-1-scaled.jpg'
            },
            {
                'title': 'Hüpfburg Delphin',
                'slug': 'huepfburg-delphin',
                'description': 'Meeresthema Hüpfburg mit Delphin-Design. Perfekt für Sommerfeste.',
                'price': 125.00,
                'category': 'huepfburgen',
                'image_file': 'hupfburg-zirkus-super-2.jpg'  # Placeholder
            },
            {
                'title': 'Hüpfburg Madagaskar',
                'slug': 'huepfburg-madagaskar',
                'description': 'Exotische Madagaskar-Hüpfburg mit wilden Tieren. Einzigartiges Design.',
                'price': 140.00,
                'category': 'huepfburgen',
                'image_file': 'Dschungel-1.jpg'  # Placeholder
            },
            {
                'title': 'Hüpfburg Party',
                'slug': 'huepfburg-party',
                'description': 'Bunte Party-Hüpfburg mit Konfetti-Design. Ideal für Feiern.',
                'price': 135.00,
                'category': 'huepfburgen',
                'image_file': 'hupfburg-zirkus-super-2.jpg'  # Placeholder
            },
            {
                'title': 'Riesen Rutsche',
                'slug': 'riesen-rutsche',
                'description': 'Große Rutsche für Events. Sicher und unterhaltsam für alle Altersgruppen.',
                'price': 80.00,
                'category': 'huepfburgen',
                'image_file': 'hupfburg-zirkus-super-2.jpg'  # Placeholder
            },
            {
                'title': 'Hüpfburg Maxi',
                'slug': 'huepfburg-maxi',
                'description': 'Extra große Hüpfburg für viele Kinder. Maximale Kapazität.',
                'price': 180.00,
                'category': 'huepfburgen',
                'image_file': 'hupfburg-zirkus-super-2.jpg'  # Placeholder
            },
            {
                'title': 'Hüpfburg Shooting Combo',
                'slug': 'huepfburg-shooting-combo',
                'description': 'Hüpfburg mit integriertem Schießstand. Doppelter Spaß.',
                'price': 160.00,
                'category': 'huepfburgen',
                'image_file': 'Shooting-Combo.jpg'  # Placeholder
            },
            
            # Gesellschaftsspiele Category
            {
                'title': 'Tor mit Radar',
                'slug': 'tor-mit-radar',
                'description': 'Fußballtor mit Geschwindigkeitsmessung. Professionelle Ausrüstung.',
                'price': 90.00,
                'category': 'gesellschaftsspiele',
                'image_file': 'Fussball-Billiard-1.jpeg'  # Placeholder
            },
            {
                'title': 'Fußball-Billiard',
                'slug': 'fussball-billiard',
                'description': 'Kombination aus Fußball und Billard. Einzigartiges Spielgerät für Events.',
                'price': 90.00,
                'category': 'gesellschaftsspiele',
                'image_file': 'Fussball-Billiard-1.jpeg'
            },
            {
                'title': 'Darts XXL',
                'slug': 'darts-xxl',
                'description': 'Großes Dart-Spiel für Erwachsene und Jugendliche. Professionelle Ausrüstung.',
                'price': 80.00,
                'category': 'gesellschaftsspiele',
                'image_file': 'Dart-XXL1.jpg'
            },
            {
                'title': 'XXL Schach',
                'slug': 'xxl-schach',
                'description': 'Riesiges Schachspiel für draußen. Perfekt für Parks und Events.',
                'price': 70.00,
                'category': 'gesellschaftsspiele',
                'image_file': 'XXL-Schach-Play-Jump-1-scaled.jpg'
            },
            {
                'title': 'Stockfangen',
                'slug': 'stockfangen',
                'description': 'Traditionelles Stockfangen-Spiel. Spaß für die ganze Familie.',
                'price': 60.00,
                'category': 'gesellschaftsspiele',
                'image_file': 'XXL-Schach-Play-Jump-1-scaled.jpg'  # Placeholder
            },
            {
                'title': 'Kickertisch',
                'slug': 'kickertisch',
                'description': 'Professioneller Kickertisch für Events. Hochwertige Ausführung.',
                'price': 100.00,
                'category': 'gesellschaftsspiele',
                'image_file': 'Fussball-Billiard-1.jpeg'  # Placeholder
            },
            {
                'title': '4 gewinnt XXL',
                'slug': '4-gewinnt-xxl',
                'description': 'Riesiges 4 gewinnt Spiel für draußen. Strategisches Denken.',
                'price': 75.00,
                'category': 'gesellschaftsspiele',
                'image_file': 'XXL-Schach-Play-Jump-1-scaled.jpg'  # Placeholder
            },
            {
                'title': 'Bull Rodeo',
                'slug': 'bull-rodeo',
                'description': 'Spannendes Bull Rodeo Spiel. Action und Spaß für alle.',
                'price': 85.00,
                'category': 'gesellschaftsspiele',
                'image_file': 'Shooting-Combo.jpg'  # Placeholder
            },
            
            # Fun Food Category
            {
                'title': 'Popcornmaschine',
                'slug': 'popcornmaschine',
                'description': 'Professionelle Popcorn-Maschine für Events. Frisches Popcorn für alle Gäste.',
                'price': 60.00,
                'category': 'fun-food',
                'image_file': 'POpcornmaschine-Rastatt-1.jpg'
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