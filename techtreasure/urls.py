from django.urls import path
from techtreasure import views



app_name = 'techtreasure'

urlpatterns = [
    path('', views.home, name='home'),
    path('faqs/', views.faqs, name='faqs'),
    path('categories/', views.categories, name='categories'),
    path('login/', views.user_login, name='user_login'),
    path('categories/searchlistings/', views.searchlistings, name='searchlistings'),
    path('categories/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('categories/<slug:category_name_slug>/<int:listing_id>/', views.show_listing, name='show_listing'),
    path('all_listings/', views.all_listings, name='all_listings'),
    path('404/', views.show_404, name='404'),
    path('add_listing/', views.add_listing, name='add_listing'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register, name='register'),
    path('search/', views.search, name='search'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('history/', views.history, name='history'),
    path('accept_offer/', views.accept_offer, name='accept_offer'),
    
]