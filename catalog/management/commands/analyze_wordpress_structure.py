from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
import os
import re

class Command(BaseCommand):
    help = 'Analyze WordPress structure to understand Angebot vs Verleih'

    def add_arguments(self, parser):
        parser.add_argument('--xml-file', type=str, default='Backup/playampjump.WordPress.2025-07-24.xml')

    def handle(self, *args, **options):
        xml_file = options['xml_file']
        
        if not os.path.exists(xml_file):
            self.stdout.write(self.style.ERROR(f'XML file not found: {xml_file}'))
            return
            
        self.stdout.write('Analyzing WordPress structure...')
        
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
        
        # Analyze pages and posts
        pages = []
        posts = []
        attachments = []
        
        for item in root.findall('.//item'):
            post_type = item.find('wp:post_type', namespaces)
            if post_type is None:
                continue
                
            post_type_text = post_type.text
            
            title_elem = item.find('title')
            title = title_elem.text if title_elem is not None else 'No title'
            
            post_name = item.find('wp:post_name', namespaces)
            slug = post_name.text if post_name is not None else 'No slug'
            
            status = item.find('wp:status', namespaces)
            status_text = status.text if status is not None else 'No status'
            
            if post_type_text == 'page':
                pages.append({
                    'title': title,
                    'slug': slug,
                    'status': status_text
                })
            elif post_type_text == 'post':
                posts.append({
                    'title': title,
                    'slug': slug,
                    'status': status_text
                })
            elif post_type_text == 'attachment':
                attachments.append({
                    'title': title,
                    'slug': slug,
                    'status': status_text
                })
        
        self.stdout.write(f'\n=== PAGES ({len(pages)}) ===')
        for page in pages:
            if page['status'] == 'publish':
                self.stdout.write(f"• {page['title']} (slug: {page['slug']})")
        
        self.stdout.write(f'\n=== POSTS ({len(posts)}) ===')
        for post in posts:
            if post['status'] == 'publish':
                self.stdout.write(f"• {post['title']} (slug: {post['slug']})")
        
        self.stdout.write(f'\n=== ATTACHMENTS ({len(attachments)}) ===')
        for attachment in attachments:
            if attachment['status'] == 'inherit':
                self.stdout.write(f"• {attachment['title']} (slug: {attachment['slug']})")
        
        # Look for specific patterns
        self.stdout.write('\n=== ANALYSIS ===')
        
        # Look for Verleih page
        verleih_page = None
        for page in pages:
            if 'verleih' in page['title'].lower() or 'verleih' in page['slug'].lower():
                verleih_page = page
                break
        
        if verleih_page:
            self.stdout.write(f'Found Verleih page: {verleih_page["title"]}')
            
            # Get content of Verleih page
            for item in root.findall('.//item'):
                post_name = item.find('wp:post_name', namespaces)
                if post_name is not None and post_name.text == verleih_page['slug']:
                    content_elem = item.find('content:encoded', namespaces)
                    if content_elem is not None and content_elem.text:
                        content = content_elem.text
                        self.stdout.write(f'\nVerleih page content preview:')
                        self.stdout.write(content[:500] + '...')
                        break
        
        # Look for Angebot page
        angebot_page = None
        for page in pages:
            if (page['title'] and 'angebot' in page['title'].lower()) or (page['slug'] and 'angebot' in page['slug'].lower()):
                angebot_page = page
                break
        
        if angebot_page:
            self.stdout.write(f'\nFound Angebot page: {angebot_page["title"]}')
        
        # Look for product-related pages
        product_pages = []
        for page in pages:
            if any(keyword in page['title'].lower() for keyword in ['hüpfburg', 'huepfburg', 'spiel', 'game', 'maschine']):
                product_pages.append(page)
        
        if product_pages:
            self.stdout.write(f'\n=== PRODUCT-RELATED PAGES ({len(product_pages)}) ===')
            for page in product_pages:
                if page['status'] == 'publish':
                    self.stdout.write(f"• {page['title']} (slug: {page['slug']})")
        
        self.stdout.write(self.style.SUCCESS('\nAnalysis completed!')) 