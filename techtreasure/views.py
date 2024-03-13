from django.shortcuts import render
from django.db.models import Count
from techtreasure.models import Category, Listing, User, Offer
from techtreasure.forms import CategoryForm
from django.shortcuts import redirect
from django.http import HttpResponse
from datetime import datetime
from techtreasure.forms import UserForm, UserProfileForm

# Create your views here.
def home(request):
    category_list = Category.objects.annotate(number_of_listings=Count('listing')).order_by('-number_of_listings')[:4]
    recent_listings = Listing.objects.order_by('-creation_date')[:4]
    
    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['listings'] = recent_listings

    # request.session.set_test_cookie()
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    
    response = render(request, 'techtreasure/home.html', context=context_dict)
    # response.set_cookie('visits', 'blue', max_age=3600)
    return response

def faqs(request):
    
    visitor_cookie_handler(request)

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['visits'] = request.session['visits']

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
    
    if context_dict['category']==None:
        response = render(request, 'techtreasure/404_page.html')
    else:
        response = render(request, 'techtreasure/category.html', context=context_dict)
    return response

def show_listing(request, category_name_slug, listing_id):
    context_dict = {}
    try:
        listing = Listing.objects.get(id=listing_id)
        context_dict['listing'] = listing
    except Listing.DoesNotExist:
        context_dict['listing'] = None

    if context_dict['listing']==None:
        response = render(request, 'techtreasure/404_page.html')
    else:
        response = render(request, 'techtreasure/listing.html', context=context_dict)
    return response

def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'techtreasure/signup.html', {'user_form': user_form, 'profile_form': profile_form, 'signup': signup})

   

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('techtreasure:index'))
            else:
                return HttpResponse("Your techtreasure account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')
   
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

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        # Set the last visit cookie
        request.session['last_visit'] = last_visit_cookie
        
        # Update/set the visits cookie
    request.session['visits'] = visits



def show_404(request):
    return render(request, 'techtreasure/404_page.html')