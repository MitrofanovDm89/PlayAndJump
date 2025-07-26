# Play & Jump

Play & Jump is a small demonstration shop built with **Django** and **Tailwind CSS**. Products are organised in categories and can be added to a shopping cart. The project also contains a simple page model and a management command to import pages from a WordPress export.

## Requirements

- Python 3.12+
- Node.js 18+ (for Tailwind compilation)

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Install Tailwind and build tools:
   ```bash
   cd theme/static_src
   npm install
   ```

## Database setup

Apply the migrations before running the server:

```bash
python manage.py migrate
```

## Tailwind CSS

For development you can watch the Tailwind files:

```bash
cd theme/static_src
npm run dev
```

For a one‑time build (used for production) run:

```bash
npm run build
```

The compiled CSS will appear in `theme/static/css/dist/`.

## Running the development server

Start Django's built in server after the dependencies and migrations are applied:

```bash
python manage.py runserver
```

You can then access the site at <http://localhost:8000/>.

## WordPress XML import

Pages exported from WordPress can be imported with the `import_wp` management command. Provide the path to the XML file created via WordPress Tools → Export:

```bash
python manage.py import_wp path/to/export.xml
```

Each `<item>` with type `page` will be converted into a `Page` model instance. Existing pages with the same slug are updated.


### Importing products

Products from the WordPress export can be loaded with the `import_wp_products` command:

```bash
python manage.py import_wp_products Backup/playampjump.WordPress.2025-07-24.xml
```

This will create the default categories and populate the catalog with items using images from `Backup/used_images`.
