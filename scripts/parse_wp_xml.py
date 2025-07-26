import xml.etree.ElementTree as ET
import json
import argparse

NAMESPACES = {
    'excerpt': 'http://wordpress.org/export/1.2/excerpt/',
    'content': 'http://purl.org/rss/1.0/modules/content/',
    'wfw': 'http://wellformedweb.org/CommentAPI/',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'wp': 'http://wordpress.org/export/1.2/'
}

def parse_pages(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    channel = root.find('channel')
    pages = []
    for item in channel.findall('item'):
        post_type = item.find('wp:post_type', NAMESPACES)
        status = item.find('wp:status', NAMESPACES)
        if post_type is not None and post_type.text == 'page' and \
                status is not None and status.text == 'publish':
            page = {
                'title': item.findtext('title', default=''),
                'slug': item.findtext('wp:post_name', default='', namespaces=NAMESPACES),
                'link': item.findtext('link', default=''),
                'content': item.findtext('content:encoded', default='', namespaces=NAMESPACES)
            }
            pages.append(page)
    return pages

def main():
    parser = argparse.ArgumentParser(description='Parse WordPress XML export')
    parser.add_argument('xml', help='Path to XML file')
    parser.add_argument('-o', '--output', default='pages.json', help='Output JSON file')
    args = parser.parse_args()
    pages = parse_pages(args.xml)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(pages)} pages to {args.output}")

if __name__ == '__main__':
    main()
