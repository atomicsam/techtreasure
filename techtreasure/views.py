from django.shortcuts import render
from django.db.models import Count
from techtreasure.models import Category, Listing, User, Offer
from techtreasure.forms import CategoryForm
from django.shortcuts import redirect
from django.http import HttpResponse

# Create your views here.
def home(request):
    category_list = Category.objects.annotate(number_of_listings=Count('listing')).order_by('-number_of_listings')[:4]
    recent_listings = Listing.objects.order_by('-creation_date')[:4]
    
    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['listings'] = recent_listings
    
    request.session.set_test_cookie()
    
    response = render(request, 'techtreasure/home.html', context=context_dict)
    response.set_cookie('favorite_color', 'blue', max_age=3600)
    return response

def faqs(request):
    
    favorite_color = request.COOKIES.get('favorite_color', 'Not set')

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['favorite_color'] = favorite_color
    
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
    if request.method == 'POST':
        username = request.POST.get('username')
        request.session['user_name'] = username
        
        if request.session.test_cookie_worked():
            print("TEST COOKIE WORKED!")
            request.session.delete_test_cookie()
            
        return redirect('home')
    else:
        context_dict = {}
        context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    
    return render(request, 'techtreasure/login.html', context=context_dict)

def searchlistings(request):

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    
    response = render(request, 'techtreasure/searchlistings.html', context=context_dict)
    return response
def add_category(request):
    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/techtreasure/')
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'techtreasure/add_category.html', {'form': form})

def profile(request):
    user_name = request.session.get('user_name', 'Anonymous')
    user_email = request.session.get('user_email', 'No email provided')
    
    context = {
        'user_name': user_name,
        'user_email': user_email,
    }
    return render(request, 'techtreasure/profile.html', context)


