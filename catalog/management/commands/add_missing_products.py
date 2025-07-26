from django.core.management.base import BaseCommand
from catalog.models import Product, Category
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Add missing products from WordPress'

    def handle(self, *args, **options):
        self.stdout.write('Adding missing products...')
        
        # Missing products data from WordPress
        missing_products = {
            'huepfburg-delphin': {
                'title': 'Hüpfburg Delphin',
                'category': 'Hüpfburg',
                'price': 150,
                'image': 'Delphin-1.jpg',
                'description': 'Schöne und stabile Hüpfburg für Mädchen und Jungen. Sehr gemütliche Drucke auf der Seite fallen auf und erfreuen das Auge.',
                'specs': 'Maße: 4,5x5x4 m (LxBxH), Gewicht: 114 kg, Kapazität: 8 Kinder, Aufbauzeit: 10 Minuten, Zubehör: elektrisches Gebläse 1,1 kW, Unterlegeplane, Kabeltrommel 25m'
            },
            'fussball-darts': {
                'title': 'Fußball Darts',
                'category': 'Gesellschaftsspiele',
                'price': 99,
                'image': 'Fussball-Darts-1.jpg',
                'description': 'Jeder kann schießen, aber wer trifft die Mitte?',
                'specs': 'Größe: 3.0m x 1.2m x 3.0m, Zubehör: elektrische Pumpe, spezielle Bälle, Unterlage Plane, Kabel 25m'
            },
            'xxl-schach': {
                'title': 'XXL SCHACH',
                'category': 'Gesellschaftsspiele',
                'price': 80,
                'image': 'XXL-Schach-Play-Jump.jpg',
                'description': 'Gemeinsame Treffen mit Familie und Freunden können jetzt durch spektakulärer Spiel angenehmer gestaltet werden.',
                'specs': 'Maße: 3m x 3m, Gewicht: ca.30 kg, Aufbauzeit: 10 Minuten, Benötigte Personen: 2'
            }
        }
        
        # Get categories
        categories = {}
        for category_name in ['Hüpfburg', 'Gesellschaftsspiele', 'Fun Food']:
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': category_name.lower().replace(' ', '-')}
            )
            categories[category_name] = category
        
        # Add missing products
        added_count = 0
        for slug, data in missing_products.items():
            # Check if product already exists
            if Product.objects.filter(slug=slug).exists():
                self.stdout.write(f'Product {data["title"]} already exists, skipping...')
                continue
            
            # Get category
            category = categories[data['category']]
            
            # Create product
            product = Product.objects.create(
                title=data['title'],
                slug=slug,
                description=f"{data['description']}\n\n{data['specs']}",
                price=data['price'],
                category=category,
                is_active=True
            )
            
            # Set image if exists
            image_path = os.path.join(settings.MEDIA_ROOT, 'products', data['image'])
            if os.path.exists(image_path):
                product.image = f'products/{data["image"]}'
                product.save()
                self.stdout.write(f'✓ Set image for {product.title}')
            else:
                self.stdout.write(f'⚠ Image not found for {product.title}: {data["image"]}')
            
            added_count += 1
            self.stdout.write(f'✓ Added: {product.title} - {product.price}€')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {added_count} products!'))
        
        # Show final count
        total_products = Product.objects.count()
        self.stdout.write(f'Total products in database: {total_products}') 