import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_project.settings')

import django
django.setup()

from techtreasure.models import Category, Listing, Offer
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

Category.objects.all().delete()
Listing.objects.all().delete()
Offer.objects.all().delete()


def populate():
    # Example category data
    print("Test: " + settings.MEDIA_ROOT+'\cpu.jpg')
    categories = [
        {'name': 'CPU', 'views': 100},
        {'name': 'RAM', 'views': 50},
        {'name': 'Cooling', 'views': 20},
        {'name': 'Motherboard', 'views': 30},
        {'name': 'GPU', 'views': 80},
        {'name': 'Power Supply', 'views': 25},
        {'name': 'Peripherals', 'views': 55},
        {'name': 'Storage', 'views': 70},
        # Add more categories as needed
    ]

    # Example listings data
    listings = [
        {'name': 'Intel Core i7', 'category': 'CPU', 'description_field': 'High performance CPU', 'suggested_price': 320.00, 'location': 'London', 'itemsold': False, 'creation_date': timezone.now(), 'picture_field': 'listings/cpu.jpg'},
        {'name': 'Ryzen 5 5600', 'category': 'CPU', 'description_field': 'High performance CPU, barely used', 'suggested_price': 310.00, 'location': 'Edinburgh', 'itemsold': False, 'creation_date': timezone.now(), 'picture_field': 'listings/ryzen5600.jpg'},
        {'name': 'Corsair Vengeance LPX', 'category': 'RAM', 'description_field': 'High performance RAM', 'suggested_price': 60.00, 'location': 'New York', 'itemsold': False, 'creation_date': timezone.now(), 'picture_field': 'listings/ram.jpg'},
        {'name': 'Noctua NH-D15', 'category': 'Cooling', 'description_field': 'Efficient cooling system', 'suggested_price': 90.00, 'location': 'Berlin', 'itemsold': False, 'creation_date': timezone.now(), 'picture_field': 'listings/cooling.jpg'},
        {'name': 'ASUS ROG Strix', 'category': 'Motherboard', 'description_field': 'Feature-rich motherboard', 'suggested_price': 200.00, 'location': 'Tokyo', 'itemsold': False, 'creation_date': timezone.now(), 'picture_field': 'listings/motherboard.jpg'},
        {'name': 'RX 6700XT', 'category': 'GPU', 'description_field': 'Powerful graphics card', 'suggested_price': 470.00, 'location': 'San Francisco', 'itemsold': False, 'creation_date': timezone.now(), 'picture_field': 'listings/gpu.jpg'},  # Updated entry
        {'name': 'EVGA Supernova 750 G5', 'category': 'Power Supply', 'description_field': 'Reliable power supply', 'suggested_price': 120.00, 'location': 'London', 'itemsold': False, 'creation_date': timezone.now(), 'picture_field': 'listings/powersupply.jpg'},
        {'name': 'Logitech G502', 'category': 'Peripherals', 'description_field': 'High precision gaming mouse', 'suggested_price': 50.00, 'location': 'Paris', 'itemsold': False, 'creation_date': timezone.now(), 'picture_field': 'listings/peripherals.jpg'},
        {'name': 'Samsung 970 EVO Plus SSD', 'category': 'Storage', 'description_field': 'Fast storage solution', 'suggested_price': 100.00, 'location': 'Seoul', 'itemsold': False, 'creation_date': timezone.now(), 'picture_field': 'listings/storage.jpg'},
        # Add more listings as needed
    ]
    

    # Example offers data
    offers = [
        {'listing': 'Intel Core i7', 'price': 300.00, 'offer_date': timezone.now(), 'user': User.objects.get(pk=1)},
        {'listing': 'Corsair Vengeance LPX', 'price': 55.00, 'offer_date': timezone.now(), 'user': User.objects.get(pk=1)},
        {'listing': 'Noctua NH-D15', 'price': 85.00, 'offer_date': timezone.now(), 'user': User.objects.get(pk=1)},
        {'listing': 'ASUS ROG Strix', 'price': 190.00, 'offer_date': timezone.now(), 'user': User.objects.get(pk=1)},
        {'listing': 'RX 6700XT', 'price': 450.00, 'offer_date': timezone.now(), 'user': User.objects.get(pk=1)},
        {'listing': 'EVGA Supernova 750 G5', 'price': 110.00, 'offer_date': timezone.now(), 'user': User.objects.get(pk=1)},
        {'listing': 'Logitech G502', 'price': 45.00, 'offer_date': timezone.now(), 'user': User.objects.get(pk=1)},
        {'listing': 'Samsung 970 EVO Plus SSD', 'price': 95.00, 'offer_date': timezone.now(), 'user': User.objects.get(pk=1)},
        # Add more offers as needed
    ]
    

    # Create and add categories to the database
    for cat_data in categories:
        cat = add_category(cat_data['name'], cat_data['views'])

    # Create and add listings to the database, associating them with categories
    for listing_data in listings:
        cat = Category.objects.get(name=listing_data['category'])
        add_listing(listing_data, cat)

    # Create and add offers to the database, associating them with listings
    for offer_data in offers:
        listing = Listing.objects.get(name=offer_data['listing'])
        add_offer(offer_data, listing)

def add_category(name, views):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.save()
    return c

def add_listing(listing_data, category):
    defaults = {
        'description_field': listing_data['description_field'],
        'suggested_price': listing_data['suggested_price'],
        'location': listing_data['location'],
        'itemsold': listing_data['itemsold'],
        'creation_date': listing_data['creation_date'],
        'picture_field': listing_data['picture_field'],
    }
    l, created = Listing.objects.get_or_create(name=listing_data['name'], category=category, defaults=defaults)
    if created:
        print(f"Created listing {l.name} in category {category.name}")
    else:
        print(f"Listing {l.name} already exists")
    return l


def add_offer(offer_data, listing):
    defaults = {
        'offer_date': offer_data['offer_date']
    }
    o, created = Offer.objects.get_or_create(listing=listing, price=offer_data['price'], users=offer_data['user'], defaults=defaults)
    if created:
        print(f"Created offer for listing {listing.name} at price {offer_data['price']}")
    else:
        print(f"Offer already exists for listing {listing.name}")
    return o


# Start execution here!
if __name__ == '__main__':
    print('Starting techtreasure population script...')
    populate()
