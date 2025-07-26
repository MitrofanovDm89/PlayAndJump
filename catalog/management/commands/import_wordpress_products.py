from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
import os
import re
from catalog.models import Category, Product
from django.conf import settings
import shutil

class Command(BaseCommand):
    help = 'Import products from WordPress XML with real data'

    def add_arguments(self, parser):
        parser.add_argument('--xml-file', type=str, default='Backup/playampjump.WordPress.2025-07-24.xml')
        parser.add_argument('--clear-existing', action='store_true', help='Clear existing products before import')

    def handle(self, *args, **options):
        xml_file = options['xml_file']
        clear_existing = options['clear_existing']
        
        if not os.path.exists(xml_file):
            self.stdout.write(self.style.ERROR(f'XML file not found: {xml_file}'))
            return
            
        self.stdout.write('Starting WordPress products import...')
        
        # Clear existing products if requested
        if clear_existing:
            self.stdout.write('Clearing existing products...')
            Product.objects.all().delete()
            self.stdout.write('Existing products cleared')
        
        # Parse XML with namespace
        namespaces = {
            'wp': 'http://wordpress.org/export/1.2/',
            'content': 'http://purl.org/rss/1.0/modules/content/',
            'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
            'dc': 'http://purl.org/dc/elements/1.1/',
            'wfw': 'http://wellformedweb.org/CommentAPI/'
        }
        
        tree = ET.parse(xml_file)
        root = tree.getroot()
        
        # Define product mappings based on extracted data
        product_mappings = {
            'huepfburg-zirkus': {
                'title': 'Hüpfburg Zirkus',
                'category': 'Hüpfburg',
                'description': 'Die kleinste Hüpfburg in unserem Arsenal. Schöne Drucke im Inneren und stabile Wände sorgen für guten und sicheren Spielspaß.',
                'specs': 'Maße: 4x3x3m (LxBxH), Gewicht: 78kg, Kapazität: 6 Kinder, Aufbauzeit: 10 Minuten',
                'price': 99,
                'image': 'hupfburg-zirkus-super-1-940x652-1.jpg'
            },
            'huepfburg-dschungel': {
                'title': 'Hüpfburg Dschungel',
                'category': 'Hüpfburg',
                'description': 'Eine farbenfrohe und optisch ansprechende Hüpfburg mit Rutsche und zwei Mittelsäulen.',
                'specs': 'Maße: 4,2 x 4,7 x 2,8 m (L x B x H), Gewicht: 88 kg, Kapazität: 6 Kinder',
                'price': 130,
                'image': 'Dschungel-Hüpfburgjpg-1024x766-1.jpg'
            },
            'huepfburg-polizei': {
                'title': 'Hüpfburg Polizei',
                'category': 'Hüpfburg',
                'description': 'Manchmal ist ein Eingreifen der Polizei erforderlich, um eine Party zu beruhigen.',
                'specs': 'Länge 5m, Breite 4m, Höhe 4m, Anzahl Spieler 9, Max. Größe Spieler 1,8m',
                'price': 150,
                'image': 'POlizei-Huepfburg-1-771x1024.jpg'
            },
            'huepfburg-madagaskar': {
                'title': 'Hüpfburg Madagaskar',
                'category': 'Hüpfburg',
                'description': 'Bitte bereiten Sie sich auf verrückten Spaß mit lächelnden Tieren vor.',
                'specs': 'Maße: 5,9 x 3,8 x 3,6 m (L x B x H), Gewicht: 98 kg, Kapazität: 10 Kinder',
                'price': 150,
                'image': 'Madagaskar-Hüpfburg-1024x766-1.jpg'
            },
            'huepfburg-party': {
                'title': 'Hüpfburg Party',
                'category': 'Hüpfburg',
                'description': 'Die schöne Hüpfburg bietet nicht nur viel Spass, sondern auch Sicherheit.',
                'specs': 'Maße: 5,9 x 3,7 x 2,8 m (L x B x H), Gewicht: 110 kg, Kapazität: 12 Kinder',
                'price': 220,
                'image': 'Party-1.jpg'
            },
            'huepfburg-maxi': {
                'title': 'HÜPFBURG MAXI',
                'category': 'Hüpfburg',
                'description': 'Maxi Hüpfburg bietet Platz für 14 hüpfende Kinder gleichzeitig.',
                'specs': 'Maße: 6,6 x 5,0 x 4,1 m (L x B x H), Gewicht: 180 kg, Kapazität: 14 Kinder',
                'price': 250,
                'image': 'Maxi-Hüpfburg1-1024x766-1.jpg'
            },
            'shooting-combo': {
                'title': 'SHOOTING COMBO',
                'category': 'Hüpfburg',
                'description': 'Kann man nur auf Hüpfburg springen? Nicht! Sie können auch die Rutsche hinunterrutschen und Kugeln aus zwei Kanonen schießen.',
                'specs': 'Maße: 6,3 x 4,5 x 5,0 m (L x B x H), Gewicht: 155 kg, Kapazität: 10 Kinder',
                'price': 300,
                'image': 'Shooting-Combo2.jpg'
            },
            'dart-xxl': {
                'title': 'DART XXL',
                'category': 'Gesellschaftsspiele',
                'description': 'Ein tolles Partyspiel in der XXL-Version. Spaß garantiert für Groß und Klein.',
                'specs': 'Maße: 2,5m x 2,3m x 2m (HxBxL), Gewicht: ca.25 kg, Aufbauzeit: 5 Minuten',
                'price': 99,
                'image': 'Dart-XXL1.jpg'
            },
            'fussball-billiard': {
                'title': 'FUSSBALL-BILLIARD',
                'category': 'Gesellschaftsspiele',
                'description': 'Kombination aus Fußball und Billiard - ein einzigartiges Spielerlebnis.',
                'specs': 'Maße: 3,5m x 2,5m x 1,2m, Gewicht: ca.45 kg, Aufbauzeit: 15 Minuten',
                'price': 120,
                'image': 'Fussball-Billiard1.jpeg'
            },
            'tor-mit-radar': {
                'title': 'Tor mit Radar',
                'category': 'Gesellschaftsspiele',
                'description': 'Fußballtor mit Geschwindigkeitsmessung - perfekt für Turniere und Events.',
                'specs': 'Maße: 3m x 2m, Gewicht: ca.35 kg, Aufbauzeit: 10 Minuten',
                'price': 80,
                'image': 'Tor-mit-Radar-1.jpg'
            },
            'stockfangen': {
                'title': 'Stockfangen',
                'category': 'Gesellschaftsspiele',
                'description': 'Klassisches Geschicklichkeitsspiel für alle Altersgruppen.',
                'specs': 'Maße: 2m x 2m, Gewicht: ca.15 kg, Aufbauzeit: 5 Minuten',
                'price': 50,
                'image': 'kregle.jpg'
            },
            'kickertisch': {
                'title': 'Kickertisch',
                'category': 'Gesellschaftsspiele',
                'description': 'Professioneller Kickertisch für spannende Turniere.',
                'specs': 'Maße: 1,4m x 0,8m x 0,9m, Gewicht: ca.40 kg, Aufbauzeit: 10 Minuten',
                'price': 90,
                'image': 'Fussball-Billiard1.jpeg'
            },
            '4-gewinnt-xxl': {
                'title': '4 gewinnt XXL',
                'category': 'Gesellschaftsspiele',
                'description': 'Strategiespiel in XXL-Größe für zwei Spieler.',
                'specs': 'Maße: 2,5m x 2,3m x 2m, Gewicht: ca.25 kg, Aufbauzeit: 5 Minuten',
                'price': 50,
                'image': 'XXL-Schach-Play-Jump.jpg'
            },
            'bull-rodeo': {
                'title': 'Bull Rodeo',
                'category': 'Gesellschaftsspiele',
                'description': 'Spannendes Spiel für mutige Teilnehmer.',
                'specs': 'Maße: 3m x 3m, Gewicht: ca.30 kg, Aufbauzeit: 10 Minuten',
                'price': 70,
                'image': 'Shooting-Combo2.jpg'
            },
            'popcornmaschine': {
                'title': 'Popcornmaschine',
                'category': 'Fun Food',
                'description': 'Professionelle Popcornmaschine für Events und Partys.',
                'specs': 'Maße: 0,8m x 0,6m x 1,2m, Gewicht: ca.25 kg, Aufbauzeit: 5 Minuten',
                'price': 60,
                'image': 'POpcornmaschine-Rastatt-1.jpg'
            }
        }
        
        # Create categories if they don't exist
        categories = {}
        for category_name in ['Hüpfburg', 'Gesellschaftsspiele', 'Fun Food']:
            category, created = Category.objects.get_or_create(
                name=category_name,
                defaults={'slug': category_name.lower().replace(' ', '-')}
            )
            categories[category_name] = category
            if created:
                self.stdout.write(f'Created category: {category_name}')
        
        # Import products
        imported_count = 0
        for slug, product_data in product_mappings.items():
            # Check if product already exists
            if Product.objects.filter(slug=slug).exists():
                self.stdout.write(f'Product {product_data["title"]} already exists, skipping...')
                continue
            
            # Get category
            category = categories[product_data['category']]
            
            # Create product
            product = Product.objects.create(
                title=product_data['title'],
                slug=slug,
                description=f"{product_data['description']}\n\n{product_data['specs']}",
                price=product_data['price'],
                category=category,
                is_active=True
            )
            
            # Set image if exists
            image_path = os.path.join(settings.MEDIA_ROOT, 'products', product_data['image'])
            if os.path.exists(image_path):
                product.image = f'products/{product_data["image"]}'
                product.save()
                self.stdout.write(f'Set image for {product.title}')
            
            imported_count += 1
            self.stdout.write(f'Imported: {product.title}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully imported {imported_count} products!')) 