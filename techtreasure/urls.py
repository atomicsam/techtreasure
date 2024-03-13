from django.urls import path
from techtreasure import views

app_name = 'techtreasure'

urlpatterns = [
    path('', views.home, name='home'),
    path('faqs/', views.faqs, name='faqs'),
    path('categories/', views.categories, name='categories'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('categories/searchlistings/', views.searchlistings, name='searchlistings'),
    path('categories/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('categories/<slug:category_name_slug>/<int:listing_id>/', views.show_listing, name='show_listing'),
    path('404/', views.show_404, name='404'),
    path('add_listing/', views.add_listing, name='add_listing'),
    path('profile/', views.profile, name='profile'),
    
]