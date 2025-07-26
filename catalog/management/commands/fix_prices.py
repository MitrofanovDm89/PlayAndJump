from django.core.management.base import BaseCommand
from catalog.models import Product

class Command(BaseCommand):
    help = 'Fix product prices based on exact WordPress data'

    def handle(self, *args, **options):
        self.stdout.write('Fixing product prices...')
        
        # Exact prices from WordPress XML
        price_fixes = {
            'fussball-billiard': 99,  # Was 120, should be 99
            'tor-mit-radar': 200,     # Was 80, should be 200
            'stockfangen': 99,        # Was 50, should be 99
            'bull-rodeo': 425,        # Was 70, should be 425
            'popcornmaschine': 79,    # Was 60, should be 79
        }
        
        updated_count = 0
        for slug, correct_price in price_fixes.items():
            try:
                product = Product.objects.get(slug=slug)
                old_price = product.price
                product.price = correct_price
                product.save()
                self.stdout.write(f'✓ Updated {product.title}: {old_price}€ → {correct_price}€')
                updated_count += 1
            except Product.DoesNotExist:
                self.stdout.write(f'❌ Product not found: {slug}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} prices!'))
        
        # Show final prices
        self.stdout.write('\nFinal prices:')
        for product in Product.objects.all().order_by('category__name', 'title'):
            self.stdout.write(f'• {product.title}: {product.price}€ ({product.category.name})') 