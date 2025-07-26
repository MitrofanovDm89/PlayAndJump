from django.core.management.base import BaseCommand
from xml.etree import ElementTree as ET
from main.models import Page

class Command(BaseCommand):
    help = "Import WordPress pages from an XML export file"

    def add_arguments(self, parser):
        parser.add_argument('xml_path', help='Path to the WordPress XML export')

    def handle(self, xml_path, **options):
        ns = {
            'content': 'http://purl.org/rss/1.0/modules/content/',
            'wp': 'http://wordpress.org/export/1.2/'
        }
        tree = ET.parse(xml_path)
        root = tree.getroot()
        count = 0
        for item in root.findall('.//item'):
            post_type = item.find('wp:post_type', ns)
            if post_type is None or post_type.text != 'page':
                continue
            title_el = item.find('title')
            slug_el = item.find('wp:post_name', ns)
            content_el = item.find('content:encoded', ns)
            title = title_el.text if title_el is not None else ''
            slug = slug_el.text if slug_el is not None else ''
            content = content_el.text if content_el is not None else ''
            if not slug:
                continue
            Page.objects.update_or_create(
                slug=slug,
                defaults={'title': title, 'content': content}
            )
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Imported {count} pages'))
