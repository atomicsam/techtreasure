from django.shortcuts import render
from django.db.models import Count
from techtreasure.models import Category, Listing, User, Offer

# Create your views here.
def home(request):
    category_list = Category.objects.annotate(number_of_listings=Count('listing')).order_by('-number_of_listings')[:4]
    recent_listings = Listing.objects.order_by('-creation_date')[:4]
    
    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['listings'] = recent_listings
    
    response = render(request, 'techtreasure/home.html', context=context_dict)
    return response

def faqs(request):

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    
    response = render(request, 'techtreasure/faqs.html', context=context_dict)
    return response

def categories(request):
    category_list = Category.objects.order_by('name')
    context_dict = {}
    
    context_dict['categories'] = category_list
    
    response = render(request, 'techtreasure/categories.html', context=context_dict)
    return response

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        listings = Listing.objects.filter(category=category)
        context_dict['listings'] = listings
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['listings'] = None
    
    response = render(request, 'techtreasure/category.html', context=context_dict)
    return response

def signup(request):

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    
    response = render(request, 'techtreasure/signup.html', context=context_dict)
    return response

def login(request):

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    
    response = render(request, 'techtreasure/login.html', context=context_dict)
    return response

def searchlistings(request):

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    
    response = render(request, 'techtreasure/searchlistings.html', context=context_dict)
    return response