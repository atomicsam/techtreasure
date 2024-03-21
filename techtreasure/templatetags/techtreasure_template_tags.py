from django import template
from techtreasure.models import Category, Listing, Offer

register = template.Library()

@register.inclusion_tag('techtreasure/list_categories.html')
def get_category_list(categories=Category.objects.all()):
    return {'categories': categories}

@register.inclusion_tag('techtreasure/list_listings.html')
def get_category_listings_list(category=None, listings=None):
    return {'listings': Listing.objects.filter(category=category)}

@register.inclusion_tag('techtreasure/list_listings.html')
def get_recent_listings(listings):
    return {'listings': listings}

@register.inclusion_tag('techtreasure/navbar_dropdown.html')
def get_all_categories():
    return {'categories': Category.objects.all().order_by("name")}

@register.inclusion_tag('techtreasure/list_listings.html')
def get_offer_listings(offers):
    listings = Listing.objects.filter(id__in=offers.values("listing"))
    return {'listings': listings}