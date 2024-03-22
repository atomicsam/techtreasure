from itertools import product
from django.shortcuts import render
from django.db.models import Count
from techtreasure.models import Category, Listing, User, Offer
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse
from datetime import datetime
from techtreasure.forms import UserForm, MakeListingForm, MakeOfferForm
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from techtreasure.bing_search import run_query
from techtreasure.models import Listing
from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator



# Create your views here.
def home(request):
    category_list = Category.objects.annotate(number_of_listings=Count('listing')).order_by('-number_of_listings')[:4]
    recent_listings = Listing.objects.filter(itemsold=False).order_by('-creation_date')[:4]
    
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
        listings = Listing.objects.filter(category=category, itemsold=False)
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
        context_dict['offer'] = Offer.objects.filter(listing=listing)
    except Listing.DoesNotExist:
        context_dict['listing'] = None
        context_dict['offer'] = None
    if request.method == "POST":
        form = MakeOfferForm(request.POST)
        if form.is_valid():
            offer_form = form.save(commit=False)
            offer_form.offer_date = str(datetime.now())
            offer_form.users = request.user
            offer_form.listing_id = listing_id
            offer_form.save()
        else:
            print(form.errors)
        context_dict['form'] = form
    else:
        form = MakeOfferForm()
    if context_dict['listing']==None:
        response = render(request, 'techtreasure/404_page.html')
    else:
        response = render(request, 'techtreasure/listing.html', context=context_dict)
    
    return response

def all_listings(request):
    context_dict = {}
    try:
        listing = Listing.objects.filter(itemsold=False)
        context_dict['listing'] = listing
    except Listing.DoesNotExist:
        context_dict['listing'] = None

    if context_dict['listing']==None:
        response = render(request, 'techtreasure/404_page.html')
    else:
        response = render(request, 'techtreasure/listings.html', context=context_dict)
    return response

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            registered = True
        else:
            print(user_form.non_field_errors)
    else:
        user_form = UserForm()

    return render(request, 'techtreasure/signup.html', {'user_form': user_form, 'registered': registered})

   

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('techtreasure:home'))
            else:
                return HttpResponse("Your techtreasure account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'techtreasure/login.html')
   
def searchlistings(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        # Perform the search query
        results = Listing.objects.filter(name__icontains=query, itemsold=False)
    return render(request, 'techtreasure/search_results.html', {'query': query, 'results': results})


    

@login_required
def add_listing(request):
    if request.method == 'POST':
        form = MakeListingForm(request.POST)
        if form.is_valid():
            listing_form = form.save(commit=False)
            listing_form.users = request.user
            listing_form.itemsold = False
            listing_form.creation_date = str(datetime.now())
            try:
                listing_form.picture_field = request.FILES['picture_field']
            except:
                listing_form.picture_field = 'listings/default_listing.jpg'

            listing_form.save()
            return redirect('/techtreasure/')
        else:
            print(form.errors)
    else:
        form = MakeListingForm()
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



def search(request):
    result_list = []
    if request.method == 'POST':
        query = request.POST['query'].strip()
        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)
    return render(request, 'techtreasure/search.html', {'result_list': result_list})

@login_required
def user_logout(request):

    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('techtreasure:home'))

@login_required
def dashboard_view(request):
    # Get active listings
    active_listings = Listing.objects.filter(itemsold=False, users=request.user)

    # Get active offers
    all_active_listings = Listing.objects.filter(itemsold=False)
    active_offers = Offer.objects.filter(users=request.user, listing__in=all_active_listings)

    context = {
        'active_listings': active_listings,
        'active_offers': active_offers,
    }
    return render(request, 'techtreasure/dashboard.html', context)

@login_required
def settings(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        old_pwd = request.POST.get('old_pwd')
        new_pwd = request.POST.get('new_pwd')
        user_obj = User.objects.filter(username=name, password=old_pwd).values("id", "username", "password").first()
        if user_obj:
            User.objects.filter(id=user_obj.get("id", None)).update(password=new_pwd)
            return JsonResponse({"message": "Password updated successfully", "code": 200})
        else:
            return JsonResponse({"message": "User does not exist", "code": 400})

    return render(request, 'techtreasure/password_change_form.html')

@login_required
def history(request):
     # Get active listings
    old_listings = Listing.objects.filter(itemsold=True, users=request.user)

    # Get active offers
    all_sold_listings = Listing.objects.filter(itemsold=True)
    old_offers = Offer.objects.filter(users=request.user, listing__in=all_sold_listings)

    context = {'listings': old_listings, 'offers': old_offers}
    return render(request, 'techtreasure/history.html', context)

def accept_offer(request):
    listing_id = request.POST.get('listing_id')
    offer_id = request.POST.get('offer_id')
    new_price = Offer.objects.get(id=offer_id).price
    print(type(new_price))
    if listing_id:
        Listing.objects.filter(pk=listing_id).update(itemsold=True, suggested_price=int(new_price))
    
    return redirect(reverse('techtreasure:home'))

    offer_id = int(request.POST.get("offer"))
    offer = Offer.objects.get(id=offer_id)
    print(offer.listing.itemsold)
    if request.method == "POST":
        offer_form = get_object_or_404(Offer, id=offer_id)
        offer_form.listing.itemsold = True
        offer_form.listing.suggested_price = offer.price
        offer_form.save()
    return redirect(reverse('techtreasure:home'))

# class AcceptOfferView(View):
#     @method_decorator(login_required)
#     def get(self, request):
#         if 'listing_id' in request.POST:
#             listing_id = request.POST['listing_id']
#         else:
#             listing_id = False
#         try:
#             listing = Listing.objects.get(id=int(listing_id))
#         except Listing.DoesNotExist:
#             return HttpResponse(-1)
#         except ValueError:
#             return HttpResponse(-1)
        
#         listing.itemsold = True
#         listing.save()
        
#         return HttpResponse(listing.itemsold)