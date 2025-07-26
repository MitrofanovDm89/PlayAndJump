import os
import re
from django.core.management.base import BaseCommand
from xml.etree import ElementTree as ET
from catalog.models import Category, Product
from django.core.files import File
from django.conf import settings

class Command(BaseCommand):
    help = "Import products from WordPress XML export"

    def add_arguments(self, parser):
        parser.add_argument('xml_path', help='Path to WordPress XML file')

    def handle(self, xml_path, **options):
        ns = {
            'wp': 'http://wordpress.org/export/1.2/',
            'content': 'http://purl.org/rss/1.0/modules/content/'
        }
        tree = ET.parse(xml_path)
        root = tree.getroot()
        channel = root.find('channel')

        # predefined categories
        categories = {
            'huepfburgen': 'H\u00fcpfburgen',
            'gesellschaftsspiele': 'Gesellschaftsspiele',
            'funfood': 'FunFood'
        }
        cat_objs = {}
        for slug, name in categories.items():
            cat_objs[slug], _ = Category.objects.get_or_create(slug=slug, defaults={'name': name})

        img_dir = os.path.join(settings.BASE_DIR, 'Backup', 'used_images')
        media_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        os.makedirs(media_dir, exist_ok=True)

        def guess_category(slug):
            if slug.startswith('huepfburg') or 'rutsche' in slug:
                return cat_objs['huepfburgen']
            if slug in ['dart-xxl', 'fussball-billiard', 'xxl-schach', 'kickertisch',
                         'fussball-darts', 'stockfangen', 'bull-rodeo-2',
                         'tor-mit-radar-3', '4-gewinnt-xxl', 'shooting-combo']:
                return cat_objs['gesellschaftsspiele']
            if slug in ['popcornmaschine', 'zuckerwatte']:
                return cat_objs['funfood']
            return None

        def find_image(slug):
            pattern = slug.replace('ue', 'u').lower()
            for fname in os.listdir(img_dir):
                if pattern in fname.lower():
                    return os.path.join(img_dir, fname)
            return os.path.join(img_dir, 'placeholder.png')

        count = 0
        for item in channel.findall('item'):
            if item.findtext('wp:post_type', namespaces=ns) != 'page':
                continue
            slug = item.findtext('wp:post_name', namespaces=ns)
            title = item.findtext('title')
            content = item.findtext('content:encoded', namespaces=ns) or ''
            if not slug or not title:
                continue
            category = guess_category(slug)
            if not category:
                continue

            img_path = find_image(slug)
            product, _ = Product.objects.update_or_create(
                slug=slug,
                defaults={'title': title, 'description': content, 'category': category}
            )
            with open(img_path, 'rb') as f:
                product.image.save(os.path.basename(img_path), File(f), save=True)
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Imported {count} products'))
