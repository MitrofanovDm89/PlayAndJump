from django.core.management.base import BaseCommand
from catalog.models import Product, Category
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Fix products data with exact prices and images from WordPress'

    def handle(self, *args, **options):
        self.stdout.write('Fixing products data...')
        
        # Exact product data from WordPress XML
        products_data = {
            'huepfburg-zirkus': {
                'title': 'Hüpfburg Zirkus',
                'price': 99,
                'image': 'hupfburg-zirkus-super-1-940x652-1.jpg',
                'description': 'Die kleinste Hüpfburg in unserem Arsenal. Schöne Drucke im Inneren und stabile Wände sorgen für guten und sicheren Spielspaß.',
                'specs': 'Maße: 4x3x3m (LxBxH), Gewicht: 78kg, Kapazität: 6 Kinder, Aufbauzeit: 10 Minuten, Benötigte Personen: 1, Zubehör: elektrisches Gebläse 1,1kW, Unterlegeplane, Kabeltrommel 25m'
            },
            'huepfburg-dschungel': {
                'title': 'Hüpfburg Dschungel',
                'price': 130,
                'image': 'Dschungel-Hüpfburgjpg-1024x766-1.jpg',
                'description': 'Eine farbenfrohe und optisch ansprechende Hüpfburg mit Rutsche und zwei Mittelsäulen. Die Kinder bekamen einen Ansturm.',
                'specs': 'Maße: 4,2 x 4,7 x 2,8 m (L x B x H), Gewicht: 88 kg, Kapazität: 6 Kinder, Aufbauzeit: 10 Minuten, Benötigte Personen: 1, Zubehör: elektrisches Gebläse 1,1 kW, Unterlegeplane, Kabeltrommel 25m'
            },
            'huepfburg-polizei': {
                'title': 'Hüpfburg Polizei',
                'price': 150,
                'image': 'POlizei-Huepfburg-1-771x1024.jpg',
                'description': 'Manchmal ist ein Eingreifen der Polizei erforderlich, um eine Party zu beruhigen. Wird sie dich dazu bringen, deine Kinder zu rocken?!',
                'specs': 'Länge 5m, Breite 4m, Höhe 4m, Anzahl Spieler 9, Max. Größe Spieler 1,8m, Personen für Aufbau/Abbau: 2 Personen, Gebläse 1,1 kW x 1, Gebläse = 17 kg, Zubehör: Unterlege Plane, Verlängerung Kabel, Fallschutzmatten'
            },
            'huepfburg-madagaskar': {
                'title': 'Hüpfburg Madagaskar',
                'price': 150,
                'image': 'Madagaskar-Hüpfburg-1024x766-1.jpg',
                'description': 'Bitte bereiten Sie sich auf verrückten Spaß mit lächelnden Tieren vor.',
                'specs': 'Maße: 5,9 x 3,8 x 3,6 m (L x B x H), Gewicht: 98 kg, Kapazität: 10 Kinder, Aufbauzeit: 10 Minuten, Benötigte Personen: 1-2, Zubehör: elektrisches Gebläse 1,1 kW, Unterlegeplane, Kabeltrommel 25m'
            },
            'huepfburg-party': {
                'title': 'Hüpfburg Party',
                'price': 220,
                'image': 'Party-1.jpg',
                'description': 'Die schöne Hüpfburg bietet nicht nur viel Spass, sondern auch Sicherheit. Die Rutsche befindet sich seitlich am Eingang, was das Beobachten von spielenden Kindern erleichtert.',
                'specs': 'Maße: 5,9 x 3,7 x 2,8 m (L x B x H), Gewicht: 110 kg, Kapazität: 12 Kinder, Aufbauzeit: 10 Minuten, Benötigte Personen: 1-2, Zubehör: elektrisches Gebläse 1,1 kW, Unterlegeplane, Kabeltrommel 25m'
            },
            'huepfburg-maxi': {
                'title': 'HÜPFBURG MAXI',
                'price': 250,
                'image': 'Maxi-Hüpfburg1-1024x766-1.jpg',
                'description': 'Maxi Hüpfburg bietet Platz für 14 hüpfende Kinder gleichzeitig. Die perfekte Wahl für Feiern, Kindergartenfeste oder ähnliches.',
                'specs': 'Maße: 6,6 x 5,0 x 4,1 m (L x B x H), Gewicht: 180 kg, Kapazität: 14 Kinder, Aufbauzeit: 20 Minuten, Benötigte Personen: 2, Zubehör: elektrisches Gebläse 1,1kW, Unterlegeplane, Kabeltrommel 25m'
            },
            'shooting-combo': {
                'title': 'SHOOTING COMBO',
                'price': 300,
                'image': 'Shooting-Combo2.jpg',
                'description': 'Kann man nur auf Hüpfburg springen? Nicht! Sie können auch die Rutsche hinunterrutschen und Kugeln aus zwei Kanonen schießen.',
                'specs': 'Maße: 6,3 x 4,5 x 5,0 m (L x B x H), Gewicht: 155 kg, Kapazität: 10 Kinder, Aufbauzeit: 15 Minuten, 2 shooterkanonnen und 100 Bälle sind dabei, Zubehör: elektrisches Gebläse 1,1 kW, Unterlegeplane, Kabeltrommel 25m'
            },
            'dart-xxl': {
                'title': 'DART XXL',
                'price': 99,
                'image': 'Dart-XXL1.jpg',
                'description': 'Ein tolles Partyspiel in der XXL-Version. Spaß garantiert für Groß und Klein.',
                'specs': 'Maße: 2,5m x 2,3m x 2m (HxBxL), Gewicht: ca.25 kg, Aufbauzeit: 5 Minuten, Benötigte Personen: 1, Zubehör: elektrische Luftpumpe 1200 W, Kabeltrommel 25m'
            },
            'fussball-billiard': {
                'title': 'FUSSBALL-BILLIARD',
                'price': 120,
                'image': 'Fussball-Billiard1.jpeg',
                'description': 'Kombination aus Fußball und Billiard - ein einzigartiges Spielerlebnis.',
                'specs': 'Maße: 3,5m x 2,5m x 1,2m, Gewicht: ca.45 kg, Aufbauzeit: 15 Minuten, Benötigte Personen: 2'
            },
            'tor-mit-radar': {
                'title': 'Tor mit Radar',
                'price': 80,
                'image': 'Tor-mit-Radar-1.jpg',
                'description': 'Fußballtor mit Geschwindigkeitsmessung - perfekt für Turniere und Events.',
                'specs': 'Maße: 3m x 2m, Gewicht: ca.35 kg, Aufbauzeit: 10 Minuten, Benötigte Personen: 1'
            },
            'stockfangen': {
                'title': 'Stockfangen',
                'price': 50,
                'image': 'kregle.jpg',
                'description': 'Klassisches Geschicklichkeitsspiel für alle Altersgruppen.',
                'specs': 'Maße: 2m x 2m, Gewicht: ca.15 kg, Aufbauzeit: 5 Minuten, Benötigte Personen: 1'
            },
            'kickertisch': {
                'title': 'Kickertisch',
                'price': 90,
                'image': 'Kickertisch2-300x225.jpg',
                'description': 'Professioneller Kickertisch für spannende Turniere.',
                'specs': 'Maße: 1,4m x 0,8m x 0,9m, Gewicht: ca.40 kg, Aufbauzeit: 10 Minuten, Benötigte Personen: 2'
            },
            '4-gewinnt-xxl': {
                'title': '4 gewinnt XXL',
                'price': 50,
                'image': 'XXL-Schach-Play-Jump.jpg',
                'description': 'Strategiespiel in XXL-Größe für zwei Spieler.',
                'specs': 'Maße: 2,5m x 2,3m x 2m, Gewicht: ca.25 kg, Aufbauzeit: 5 Minuten, Benötigte Personen: 1'
            },
            'bull-rodeo': {
                'title': 'Bull Rodeo',
                'price': 70,
                'image': 'Bull-Rodeo-1024x517.jpg',
                'description': 'Spannendes Spiel für mutige Teilnehmer.',
                'specs': 'Maße: 3m x 3m, Gewicht: ca.30 kg, Aufbauzeit: 10 Minuten, Benötigte Personen: 1'
            },
            'popcornmaschine': {
                'title': 'Popcornmaschine',
                'price': 60,
                'image': 'POpcornmaschine-Rastatt-1.jpg',
                'description': 'Professionelle Popcornmaschine für Events und Partys.',
                'specs': 'Maße: 0,8m x 0,6m x 1,2m, Gewicht: ca.25 kg, Aufbauzeit: 5 Minuten, Benötigte Personen: 1'
            }
        }
        
        # Update products
        updated_count = 0
        for slug, data in products_data.items():
            try:
                product = Product.objects.get(slug=slug)
                
                # Update basic info
                product.title = data['title']
                product.price = data['price']
                product.description = f"{data['description']}\n\n{data['specs']}"
                
                # Check if image exists and update
                image_path = os.path.join(settings.MEDIA_ROOT, 'products', data['image'])
                if os.path.exists(image_path):
                    product.image = f'products/{data["image"]}'
                    self.stdout.write(f'✓ Image set for {product.title}: {data["image"]}')
                else:
                    self.stdout.write(f'⚠ Image not found for {product.title}: {data["image"]}')
                
                product.save()
                updated_count += 1
                self.stdout.write(f'✓ Updated: {product.title} - {product.price}€')
                
            except Product.DoesNotExist:
                self.stdout.write(f'❌ Product not found: {slug}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} products!'))
        
        # Show final status
        self.stdout.write('\nFinal products status:')
        for product in Product.objects.all():
            image_status = '✓' if product.image else '❌'
            self.stdout.write(f'{image_status} {product.title}: {product.price}€ - {product.image or "No image"}') 