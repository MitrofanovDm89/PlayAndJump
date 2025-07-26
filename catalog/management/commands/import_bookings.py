from django.core.management.base import BaseCommand
from catalog.models import Product, Booking
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Import sample bookings for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample bookings...')
        
        # Get all products
        products = Product.objects.all()
        
        if not products.exists():
            self.stdout.write(self.style.ERROR('No products found. Please run import_products first.'))
            return
        
        # Sample customer data
        customers = [
            {'name': 'Max Mustermann', 'email': 'max@example.com', 'phone': '+49 123 456789'},
            {'name': 'Anna Schmidt', 'email': 'anna@example.com', 'phone': '+49 987 654321'},
            {'name': 'Tom Weber', 'email': 'tom@example.com', 'phone': '+49 555 123456'},
            {'name': 'Lisa Müller', 'email': 'lisa@example.com', 'phone': '+49 777 888999'},
            {'name': 'Peter Fischer', 'email': 'peter@example.com', 'phone': '+49 111 222333'},
        ]
        
        # Create bookings for the next 3 months
        today = date.today()
        bookings_created = 0
        
        for product in products:
            # Create 2-4 random bookings per product
            num_bookings = random.randint(2, 4)
            
            for i in range(num_bookings):
                # Random start date within next 3 months
                days_from_today = random.randint(1, 90)
                start_date = today + timedelta(days=days_from_today)
                
                # Random duration (1-7 days)
                duration = random.randint(1, 7)
                end_date = start_date + timedelta(days=duration - 1)
                
                # Random customer
                customer = random.choice(customers)
                
                # Calculate total price
                total_price = product.price * duration if product.price else 100 * duration
                
                # Random status (mostly confirmed)
                status = random.choices(['confirmed', 'pending', 'cancelled'], weights=[70, 20, 10])[0]
                
                # Create booking
                booking, created = Booking.objects.get_or_create(
                    product=product,
                    start_date=start_date,
                    end_date=end_date,
                    defaults={
                        'customer_name': customer['name'],
                        'customer_email': customer['email'],
                        'customer_phone': customer['phone'],
                        'total_price': total_price,
                        'status': status,
                        'notes': f'Test booking {i+1} for {product.title}'
                    }
                )
                
                if created:
                    bookings_created += 1
                    self.stdout.write(f'Created booking: {booking}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {bookings_created} bookings')
        ) 