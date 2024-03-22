from django.test import TestCase,Client
from django.urls import reverse
from techtreasure.models import Category

def add_category(name, views=0):
    category = Category.objects.get_or_create(name=name)[0]
    category.views = views
    category.save()
    return category

class CategoryMethodTests(TestCase):
    def test_ensure_views_are_positive(self):
        """
        Ensures the number of views received for a Category are positive or zero.
        """
        category = Category(name='test', views=-1) 
        category.save()
        self.assertEqual((category.views >= 0), True)

    def test_slug_line_creation(self):
        """
        Checks to make sure that when a category is created, an
        appropriate slug is created.
        Example: "Random Category String" should be "random-category-string".
        """
        category = Category(name='Random Category String')
        category.save()
        self.assertEqual(category.slug, 'random-category-string')
        
class IndexViewTests(TestCase):
    def test_index_view_with_no_categories(self):
        """
        If no categories exist, the appropriate message should be displayed.
        """
        response = self.client.get(reverse('techtreasure:home'))
        self.assertEqual(response.status_code, 200)
        
        self.assertQuerysetEqual(response.context['categories'], [])

def test_index_view_with_categories(self):
    """
    Checks whether categories are displayed correctly when present.
    """
    categories = [
        'CPU',
        'RAM',
        'Cooling',
        'Motherboard',
        'GPU',
        'Power Supply',
        'Peripherals',
        'Storage',
    ]

    for category_name in categories:
        add_category(category_name, views=50)

    response = self.client.get(reverse('techtreasure:home'))
    self.assertEqual(response.status_code, 200)

    for category_name in categories:
        self.assertContains(response, category_name)

    num_categories = len(response.context['categories'])
    self.assertEquals(num_categories, len(categories))
    


class ViewTest(TestCase):
    def setUp(self):
        
        self.client = Client()

    def test_home_view(self):
        
        response = self.client.get(reverse('techtreasure:home'))

        
        self.assertEqual(response.status_code, 200)

        
        

        
        self.assertTemplateUsed(response, 'techtreasure/home.html')
