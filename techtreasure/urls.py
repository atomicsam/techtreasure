from django.urls import path
from techtreasure import views

app_name = 'techtreasure'

urlpatterns = [
    path('', views.home, name='home'),
    path('faqs/', views.faqs, name='faqs'),
    path('categories/', views.categories, name='categories'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('searchlistings/', views.searchlistings, name='searchlistings'),
]