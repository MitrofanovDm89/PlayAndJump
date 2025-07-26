from django.core.management.base import BaseCommand
from catalog.models import Product

class Command(BaseCommand):
    help = 'Check products without images'

    def handle(self, *args, **options):
        self.stdout.write('Checking products without images...')
        
        products_without_images = Product.objects.filter(image='')
        products_with_none_images = Product.objects.filter(image__isnull=True)
        
        all_products_without_images = list(products_without_images) + list(products_with_none_images)
        
        if all_products_without_images:
            self.stdout.write(f'Found {len(all_products_without_images)} products without images:')
            for product in all_products_without_images:
                self.stdout.write(f'❌ {product.title} (ID: {product.id}, Slug: {product.slug})')
        else:
            self.stdout.write('✅ All products have images!')
        
        # Show all products for reference
        self.stdout.write('\nAll products:')
        for product in Product.objects.all():
            image_status = '✅' if product.image else '❌'
            self.stdout.write(f'{image_status} {product.title}: {product.image or "No image"}') 