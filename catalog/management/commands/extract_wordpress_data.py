from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
import os
import re
from catalog.models import Category, Product
from django.conf import settings
import shutil

class Command(BaseCommand):
    help = 'Extract data from WordPress XML export file'

    def add_arguments(self, parser):
        parser.add_argument('--xml-file', type=str, default='Backup/playampjump.WordPress.2025-07-24.xml')
        parser.add_argument('--images-dir', type=str, default='Backup/used_images')

    def handle(self, *args, **options):
        xml_file = options['xml_file']
        images_dir = options['images_dir']
        
        if not os.path.exists(xml_file):
            self.stdout.write(self.style.ERROR(f'XML file not found: {xml_file}'))
            return
            
        self.stdout.write('Starting WordPress data extraction...')
        
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
        
        # Extract pages and posts
        pages_data = []
        products_data = []
        
        # Find all items
        for item in root.findall('.//item'):
            post_type = item.find('wp:post_type', namespaces)
            if post_type is None:
                continue
                
            post_type_text = post_type.text
            
            if post_type_text == 'page':
                title_elem = item.find('title')
                content_elem = item.find('content:encoded', namespaces)
                
                if title_elem is not None and content_elem is not None:
                    title = title_elem.text
                    content = content_elem.text
                    
                    if title and content:
                        post_name = item.find('wp:post_name', namespaces)
                        status = item.find('wp:status', namespaces)
                        
                        pages_data.append({
                            'title': title,
                            'content': content,
                            'post_name': post_name.text if post_name is not None else '',
                            'status': status.text if status is not None else ''
                        })
                        
            elif post_type_text == 'attachment':
                # Extract image information
                title_elem = item.find('title')
                attachment_url = item.find('wp:attachment_url', namespaces)
                
                if title_elem is not None and attachment_url is not None:
                    title = title_elem.text
                    url = attachment_url.text
                    
                    if title and url:
                        # Extract filename from URL
                        filename = url.split('/')[-1]
                        products_data.append({
                            'title': title,
                            'filename': filename,
                            'url': url
                        })
        
        self.stdout.write(f'Found {len(pages_data)} pages')
        self.stdout.write(f'Found {len(products_data)} attachments')
        
        # Save extracted data to files for analysis
        self.save_pages_data(pages_data)
        self.save_products_data(products_data)
        
        # Copy images to media directory
        self.copy_images_to_media(images_dir)
        
        self.stdout.write(self.style.SUCCESS('WordPress data extraction completed!'))

    def save_pages_data(self, pages_data):
        """Save pages data to a file for analysis"""
        output_file = 'extracted_pages.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            for page in pages_data:
                f.write(f"=== {page['title']} ===\n")
                f.write(f"Slug: {page['post_name']}\n")
                f.write(f"Status: {page['status']}\n")
                f.write(f"Content: {page['content'][:500]}...\n")
                f.write("\n" + "="*50 + "\n\n")
        
        self.stdout.write(f'Pages data saved to {output_file}')

    def save_products_data(self, products_data):
        """Save products data to a file for analysis"""
        output_file = 'extracted_products.txt'
        with open(output_file, 'w', encoding='utf-8') as f:
            for product in products_data:
                f.write(f"Title: {product['title']}\n")
                f.write(f"Filename: {product['filename']}\n")
                f.write(f"URL: {product['url']}\n")
                f.write("\n" + "-"*30 + "\n\n")
        
        self.stdout.write(f'Products data saved to {output_file}')

    def copy_images_to_media(self, images_dir):
        """Copy images from backup to media directory"""
        if not os.path.exists(images_dir):
            self.stdout.write(self.style.WARNING(f'Images directory not found: {images_dir}'))
            return
            
        media_products_dir = os.path.join(settings.MEDIA_ROOT, 'products')
        os.makedirs(media_products_dir, exist_ok=True)
        
        copied_count = 0
        for filename in os.listdir(images_dir):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                src_path = os.path.join(images_dir, filename)
                dst_path = os.path.join(media_products_dir, filename)
                
                if not os.path.exists(dst_path):
                    shutil.copy2(src_path, dst_path)
                    copied_count += 1
        
        self.stdout.write(f'Copied {copied_count} images to media directory') 