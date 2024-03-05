from django.urls import path
from techtreasure import views

app_name = 'techtreasure'

urlpatterns = [
    path('', views.index, name='index'),
    path('faqs/', views.faqs, name='faqs'),
]