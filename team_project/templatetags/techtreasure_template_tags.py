from django import template
from techtreasure.models import Category

register = template.Library()

@register.inclusion_tag('techtreasure/categories.html')
def get_category_list():
    return {'categories': Category.objects.all()}