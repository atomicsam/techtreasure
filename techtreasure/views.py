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

def add_listing(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/techtreasure/')
        else:
            print(form.errors)
    return render(request, 'techtreasure/add_listing.html', {'form': form})

def profile(request):
    user_name = request.session.get('user_name', 'Anonymous')
    user_email = request.session.get('user_email', 'No email provided')
    
    context = {
        'user_name': user_name,
        'user_email': user_email,
    }
    return render(request, 'techtreasure/profile.html', context)

def visitor_cookie_handler(request, response):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(request.COOKIES.get('visits', '1'))
    
    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        response.set_cookie('last_visit', str(datetime.now()))
    else:
        # Set the last visit cookie
        response.set_cookie('last_visit', last_visit_cookie)
        
        # Update/set the visits cookie
        response.set_cookie('visits', visits)



def show_404(request):
    return render(request, 'techtreasure/404_page.html')