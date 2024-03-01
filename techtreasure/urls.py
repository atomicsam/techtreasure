from django.urls import path
from techtreasure import views

app_name = 'techtreasure'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
]