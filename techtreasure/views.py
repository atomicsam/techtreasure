from django.shortcuts import render
from techtreasure.models import Category, Listing, User, Offer

# Create your views here.
def home(request):
    category_list = Category.objects.order_by('-views')[:4]

    context_dict = {}
    context_dict['categories'] = category_list
    
    response = render(request, 'techtreasure/home.html', context=context_dict)
    return response

def faqs(request):

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    
    response = render(request, 'techtreasure/faqs.html', context=context_dict)
    return response

def categories(request):
    category_list = Category.objects.order_by('-views')[:4]
    context_dict = {}
    
    context_dict['categories'] = category_list
    
    response = render(request, 'techtreasure/categories.html', context=context_dict)
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