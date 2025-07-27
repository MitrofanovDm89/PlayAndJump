from django.core.management.base import BaseCommand
from catalog.models import Service

class Command(BaseCommand):
    help = 'Добавляет услуги для страницы Vermietung'

    def handle(self, *args, **options):
        services_data = [
            {
                'title': 'RIESEN RUTSCHE',
                'description': 'Наша гигантская горка - это настоящее приключение для детей! Безопасная конструкция с мягким покрытием обеспечивает веселье без риска.',
                'price': 299.00,
                'image': 'services/rutsche.jpg'
            },
            {
                'title': 'Event Betreuung',
                'description': 'Профессиональная организация и проведение детских мероприятий. Наши аниматоры создадут незабываемую атмосферу для любого праздника.',
                'price': 199.00,
                'image': 'services/event-betreuung.jpg'
            },
            {
                'title': 'Stromerzeuger',
                'description': 'Надежный генератор для обеспечения электроэнергией всех ваших развлечений. Идеально подходит для мероприятий на открытом воздухе.',
                'price': 149.00,
                'image': 'services/stromerzeuger.jpg'
            },
            {
                'title': 'Gebläse Schalldämmung',
                'description': 'Специальное оборудование для снижения шума. Обеспечивает комфорт для окружающих во время проведения мероприятий.',
                'price': 89.00,
                'image': 'services/schalldaemmung.jpg'
            },
            {
                'title': 'Zuckerwattemaschine',
                'description': 'Сладкое развлечение для детей! Наша машина для сахарной ваты создает настоящее волшебство и радость.',
                'price': 79.00,
                'image': 'services/zuckerwatte.jpg'
            },
            {
                'title': 'Kinderschminken',
                'description': 'Профессиональный аквагрим для детей. Наши художники превратят каждого ребенка в любимого героя.',
                'price': 59.00,
                'image': 'services/kinderschminken.jpg'
            },
            {
                'title': 'Hüpfburg Delphin',
                'description': 'Надувной замок в виде дельфина - идеальное развлечение для детских праздников. Безопасно и весело!',
                'price': 199.00,
                'image': 'services/delphin.jpg'
            },
            {
                'title': 'Hüpfburg weiß',
                'description': 'Классический белый надувной замок для любого мероприятия. Просторный и безопасный для активных игр.',
                'price': 179.00,
                'image': 'services/huepfburg-weiss.jpg'
            },
            {
                'title': 'Fußball Darts',
                'description': 'Уникальная игра, сочетающая футбол и дартс. Отличное развлечение для детей и взрослых!',
                'price': 99.00,
                'image': 'services/fussball-darts.jpg'
            }
        ]

        created_count = 0
        updated_count = 0

        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                title=service_data['title'],
                defaults={
                    'description': service_data['description'],
                    'price': service_data['price'],
                    'image': service_data['image'],
                    'is_active': True
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Создана услуга: {service.title}')
                )
            else:
                # Update existing service
                service.description = service_data['description']
                service.price = service_data['price']
                service.image = service_data['image']
                service.is_active = True
                service.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Обновлена услуга: {service.title}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Готово! Создано: {created_count}, обновлено: {updated_count} услуг'
            )
        ) 