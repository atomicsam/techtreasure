from django import template
from techtreasure.models import Category

register = template.Library()

@register.inclusion_tag('techtreasure/list_categories.html')
def get_category_list(categories=Category.objects.all()):
    return {'categories': categories}

@register.inclusion_tag('techtreasure/list_listings.html')
def get_listings_list(categories=Category.objects.all()):
    return {'categories': categories}