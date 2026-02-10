"""
Management command to seed sample data for testing.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from crops.models import Crop, CropType, CropStatus
from orders.models import Order, OrderStatus

User = get_user_model()


class Command(BaseCommand):
    help = 'Seed sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')

        # Create admin if not exists
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@crops.com', 'admin123')
            admin_user.role = 'ADMIN'
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created admin user (admin/admin123)'))

        # Create farmers
        farmers = []
        for i, (uname, name) in enumerate([('farmer1', 'John Farmer'), ('farmer2', 'Jane Grower')]):
            if not User.objects.filter(username=uname).exists():
                u = User.objects.create_user(uname, f'{uname}@crops.com', 'farmer123', first_name=name.split()[0], last_name=name.split()[1], role='FARMER')
                farmers.append(u)
                self.stdout.write(f'Created farmer {uname}')
            else:
                farmers.append(User.objects.get(username=uname))

        # Create broker
        if not User.objects.filter(username='broker1').exists():
            broker = User.objects.create_user('broker1', 'broker@crops.com', 'broker123', first_name='Mike', last_name='Broker', role='BROKER')
            self.stdout.write('Created broker broker1')
        else:
            broker = User.objects.get(username='broker1')

        # Create clients
        clients = []
        for i, (uname, name) in enumerate([('client1', 'Alice Buyer'), ('client2', 'Bob Customer')]):
            if not User.objects.filter(username=uname).exists():
                u = User.objects.create_user(uname, f'{uname}@crops.com', 'client123', first_name=name.split()[0], last_name=name.split()[1], role='CLIENT')
                clients.append(u)
                self.stdout.write(f'Created client {uname}')
            else:
                clients.append(User.objects.get(username=uname))

        # Create crops
        crop_data = [
            ('Wheat', CropType.GRAIN, 5000, 2.5, 'Nebraska', 'Available wheat harvest'),
            ('Corn', CropType.GRAIN, 8000, 1.8, 'Iowa', 'Organic corn'),
            ('Tomatoes', CropType.VEGETABLE, 500, 3.0, 'California', 'Fresh tomatoes'),
            ('Rice', CropType.GRAIN, 3000, 4.0, 'Texas', 'Long grain rice'),
            ('Lentils', CropType.PULSE, 1000, 2.2, 'North Dakota', 'Red lentils'),
        ]
        for name, ctype, qty, price, loc, desc in crop_data:
            if not Crop.objects.filter(name=name, farmer=farmers[0]).exists():
                Crop.objects.create(
                    name=name, crop_type=ctype, quantity=qty, unit='kg', price=price,
                    farmer=farmers[0], location=loc, status=CropStatus.AVAILABLE, description=desc
                )
                self.stdout.write(f'Created crop {name}')
        for name, ctype, qty, price, loc, desc in [
            ('Potatoes', CropType.VEGETABLE, 2000, 0.8, 'Idaho', 'Russet potatoes'),
            ('Apples', CropType.FRUIT, 1500, 2.0, 'Washington', 'Honeycrisp apples'),
        ]:
            if not Crop.objects.filter(name=name, farmer=farmers[1]).exists():
                Crop.objects.create(
                    name=name, crop_type=ctype, quantity=qty, unit='kg', price=price,
                    farmer=farmers[1], location=loc, status=CropStatus.AVAILABLE, description=desc
                )
                self.stdout.write(f'Created crop {name}')

        # Create sample orders
        crops = list(Crop.objects.filter(status=CropStatus.AVAILABLE)[:3])
        if crops and clients:
            for i, crop in enumerate(crops):
                if not Order.objects.filter(client=clients[0], crop=crop).exists():
                    Order.objects.create(
                        client=clients[0], crop=crop, quantity=100,
                        shipping_address='123 Main St, City, State',
                        status=OrderStatus.CONFIRMED if i == 0 else OrderStatus.PENDING
                    )
                    self.stdout.write(f'Created order for {crop.name}')

        self.stdout.write(self.style.SUCCESS('Seed data complete!'))
