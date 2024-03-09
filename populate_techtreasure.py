import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team_project.settings')

import django
django.setup()

from techtreasure.models import Category, Listing, Offer
from django.contrib.auth.models import User
from django.utils import timezone

Category.objects.all().delete()
Listing.objects.all().delete()
Offer.objects.all().delete()


def populate():
    # Example category data
    categories = [
        {'name': 'CPU', 'views': 100},
        {'name': 'RAM', 'views': 50},
        # Add more categories as needed
    ]

    # Example listings data
    listings = [
        {'name': 'Intel Core i7', 'category': 'CPU', 'description_field': 'High performance CPU', 'suggested_price': 320.00, 'location': 'London', 'itemsold': False, 'creation_date': timezone.now()},
        # Add more listings as needed
    ]

    # Example offers data
    offers = [
        {'listing': 'Intel Core i7', 'price': 300.00, 'offer_date': timezone.now()},
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
        'creation_date': listing_data['creation_date']
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
    o, created = Offer.objects.get_or_create(listing=listing, price=offer_data['price'], defaults=defaults)
    if created:
        print(f"Created offer for listing {listing.name} at price {offer_data['price']}")
    else:
        print(f"Offer already exists for listing {listing.name}")
    return o


# Start execution here!
if __name__ == '__main__':
    print('Starting techtreasure population script...')
    populate()
