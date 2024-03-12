from django import template
from techtreasure.models import Category, Listing

register = template.Library()

@register.inclusion_tag('techtreasure/list_categories.html')
def get_category_list(categories=Category.objects.all()):
    return {'categories': categories}

@register.inclusion_tag('techtreasure/list_listings.html')
def get_listings_list(listings=Listing.objects.all()):
    return {'listings': listings}

@register.inclusion_tag('techtreasure/navbar_dropdown.html')
def get_all_categories():
    return {'categories': Category.objects.all().order_by("name")}