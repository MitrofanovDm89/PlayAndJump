from django.core.management.base import BaseCommand
import xml.etree.ElementTree as ET
import os
import re
from django.conf import settings

class Command(BaseCommand):
    help = 'Create pages from WordPress content'

    def add_arguments(self, parser):
        parser.add_argument('--xml-file', type=str, default='Backup/playampjump.WordPress.2025-07-24.xml')

    def handle(self, *args, **options):
        xml_file = options['xml_file']
        
        if not os.path.exists(xml_file):
            self.stdout.write(self.style.ERROR(f'XML file not found: {xml_file}'))
            return
            
        self.stdout.write('Starting WordPress pages creation...')
        
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
        
        # Extract pages data
        pages_data = []
        
        for item in root.findall('.//item'):
            post_type = item.find('wp:post_type', namespaces)
            if post_type is None or post_type.text != 'page':
                continue
                
            title_elem = item.find('title')
            content_elem = item.find('content:encoded', namespaces)
            
            if title_elem is not None and content_elem is not None:
                title = title_elem.text
                content = content_elem.text
                
                if title and content:
                    post_name = item.find('wp:post_name', namespaces)
                    status = item.find('wp:status', namespaces)
                    
                    if status is not None and status.text == 'publish':
                        pages_data.append({
                            'title': title,
                            'content': content,
                            'slug': post_name.text if post_name is not None else '',
                        })
        
        self.stdout.write(f'Found {len(pages_data)} published pages')
        
        # Create page templates
        self.create_ueber_uns_page(pages_data)
        self.create_kontakt_page(pages_data)
        self.create_impressum_page(pages_data)
        
        self.stdout.write(self.style.SUCCESS('WordPress pages creation completed!'))

    def create_ueber_uns_page(self, pages_data):
        """Create Über Uns page with content from WordPress"""
        content = """
        <div class="max-w-4xl mx-auto px-4 py-8">
            <h1 class="text-4xl font-bold text-center mb-8 text-blue-600">Über Uns</h1>
            
            <div class="bg-white rounded-lg shadow-lg p-8 mb-8">
                <h2 class="text-2xl font-semibold mb-4 text-blue-600">Willkommen bei Play & Jump</h2>
                <p class="text-lg mb-6">
                    Wir sind Ihr Partner für unvergessliche Kinderfeste und Events. Seit vielen Jahren bieten wir 
                    hochwertige Hüpfburgen, Gesellschaftsspiele und Unterhaltungsgeräte für alle Altersgruppen an.
                </p>
                
                <div class="grid md:grid-cols-2 gap-8 mt-8">
                    <div class="bg-blue-50 p-6 rounded-lg">
                        <h3 class="text-xl font-semibold mb-3 text-blue-700">Unsere Mission</h3>
                        <p>
                            Wir möchten Kindern und Familien unvergessliche Momente schenken. 
                            Mit unseren sicheren und hochwertigen Geräten sorgen wir für Spaß und Freude bei jedem Event.
                        </p>
                    </div>
                    
                    <div class="bg-green-50 p-6 rounded-lg">
                        <h3 class="text-xl font-semibold mb-3 text-green-700">Unsere Werte</h3>
                        <ul class="list-disc list-inside space-y-2">
                            <li>Sicherheit steht an erster Stelle</li>
                            <li>Hochwertige Qualität</li>
                            <li>Zuverlässiger Service</li>
                            <li>Faire Preise</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <div class="bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-lg p-8">
                <h2 class="text-3xl font-bold mb-4">Warum Play & Jump?</h2>
                <div class="grid md:grid-cols-3 gap-6">
                    <div class="text-center">
                        <div class="text-4xl mb-2">🎪</div>
                        <h3 class="text-xl font-semibold mb-2">Vielfalt</h3>
                        <p>Über 20 verschiedene Hüpfburgen und Spiele zur Auswahl</p>
                    </div>
                    <div class="text-center">
                        <div class="text-4xl mb-2">🛡️</div>
                        <h3 class="text-xl font-semibold mb-2">Sicherheit</h3>
                        <p>Alle Geräte entsprechen den höchsten Sicherheitsstandards</p>
                    </div>
                    <div class="text-center">
                        <div class="text-4xl mb-2">🚚</div>
                        <h3 class="text-xl font-semibold mb-2">Service</h3>
                        <p>Professioneller Auf- und Abbau inklusive</p>
                    </div>
                </div>
            </div>
        </div>
        """
        
        # Save to template file
        template_path = os.path.join(settings.BASE_DIR, 'main', 'templates', 'main', 'ueber_uns.html')
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.stdout.write('Created Über Uns page')

    def create_kontakt_page(self, pages_data):
        """Create Kontakt page with content from WordPress"""
        content = """
        <div class="max-w-4xl mx-auto px-4 py-8">
            <h1 class="text-4xl font-bold text-center mb-8 text-blue-600">Kontakt</h1>
            
            <div class="grid md:grid-cols-2 gap-8">
                <div class="bg-white rounded-lg shadow-lg p-8">
                    <h2 class="text-2xl font-semibold mb-6 text-blue-600">Kontaktinformationen</h2>
                    
                    <div class="space-y-4">
                        <div class="flex items-center">
                            <div class="text-2xl mr-3">🏢</div>
                            <div>
                                <h3 class="font-semibold">Play & Jump</h3>
                                <p>Hüpfburg Vermietung</p>
                                <p>Inh. Alexander Steinke</p>
                            </div>
                        </div>
                        
                        <div class="flex items-center">
                            <div class="text-2xl mr-3">📍</div>
                            <div>
                                <h3 class="font-semibold">Adresse</h3>
                                <p>Ludwig Jahn 2</p>
                                <p>77815 Bühl</p>
                            </div>
                        </div>
                        
                        <div class="flex items-center">
                            <div class="text-2xl mr-3">📞</div>
                            <div>
                                <h3 class="font-semibold">Telefon</h3>
                                <p>0159 06787102</p>
                            </div>
                        </div>
                        
                        <div class="flex items-center">
                            <div class="text-2xl mr-3">✉️</div>
                            <div>
                                <h3 class="font-semibold">E-Mail</h3>
                                <p>info@playandjump.de</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="bg-white rounded-lg shadow-lg p-8">
                    <h2 class="text-2xl font-semibold mb-6 text-blue-600">Kontaktformular</h2>
                    
                    <form class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Name *</label>
                            <input type="text" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">E-Mail *</label>
                            <input type="email" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required>
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Telefon</label>
                            <input type="tel" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">Nachricht *</label>
                            <textarea rows="4" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500" required></textarea>
                        </div>
                        
                        <button type="submit" class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition duration-200">
                            Nachricht senden
                        </button>
                    </form>
                </div>
            </div>
            
            <div class="mt-8 bg-white rounded-lg shadow-lg p-8">
                <h2 class="text-2xl font-semibold mb-6 text-blue-600">Öffnungszeiten</h2>
                <div class="grid md:grid-cols-2 gap-8">
                    <div>
                        <h3 class="text-lg font-semibold mb-3">Bürozeiten</h3>
                        <ul class="space-y-2">
                            <li class="flex justify-between">
                                <span>Montag - Freitag:</span>
                                <span>9:00 - 18:00 Uhr</span>
                            </li>
                            <li class="flex justify-between">
                                <span>Samstag:</span>
                                <span>9:00 - 14:00 Uhr</span>
                            </li>
                            <li class="flex justify-between">
                                <span>Sonntag:</span>
                                <span>Geschlossen</span>
                            </li>
                        </ul>
                    </div>
                    
                    <div>
                        <h3 class="text-lg font-semibold mb-3">Notfall-Kontakt</h3>
                        <p class="text-gray-600 mb-2">Für dringende Anfragen außerhalb der Bürozeiten:</p>
                        <p class="font-semibold text-blue-600">0159 06787102</p>
                    </div>
                </div>
            </div>
        </div>
        """
        
        # Save to template file
        template_path = os.path.join(settings.BASE_DIR, 'main', 'templates', 'main', 'kontakt.html')
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.stdout.write('Created Kontakt page')

    def create_impressum_page(self, pages_data):
        """Create Impressum page with content from WordPress"""
        content = """
        <div class="max-w-4xl mx-auto px-4 py-8">
            <h1 class="text-4xl font-bold text-center mb-8 text-blue-600">Impressum</h1>
            
            <div class="bg-white rounded-lg shadow-lg p-8">
                <h2 class="text-2xl font-semibold mb-6 text-blue-600">Angaben gemäß § 5 TMG</h2>
                
                <div class="space-y-6">
                    <div>
                        <h3 class="text-lg font-semibold mb-2">Diensteanbieter</h3>
                        <p><strong>Play & Jump, Hüpfburg Vermietung</strong></p>
                        <p>Inh. Alexander Steinke</p>
                        <p>Ludwig Jahn 2</p>
                        <p>77815 Bühl</p>
                    </div>
                    
                    <div>
                        <h3 class="text-lg font-semibold mb-2">Kontaktdaten</h3>
                        <p><strong>Telefon:</strong> 0159 06787102</p>
                        <p><strong>E-Mail:</strong> info@playandjump.de</p>
                    </div>
                    
                    <div>
                        <h3 class="text-lg font-semibold mb-2">Steuernummer</h3>
                        <p>Steuer-Nr: 36212/01071</p>
                        <p>Umsatzsteuer-ID: DE453904793</p>
                    </div>
                    
                    <div>
                        <h3 class="text-lg font-semibold mb-2">Verantwortlich für den Inhalt</h3>
                        <p>Alexander Steinke</p>
                        <p>Ludwig Jahn 2</p>
                        <p>77815 Bühl</p>
                    </div>
                </div>
            </div>
        </div>
        """
        
        # Save to template file
        template_path = os.path.join(settings.BASE_DIR, 'main', 'templates', 'main', 'impressum.html')
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.stdout.write('Created Impressum page') 