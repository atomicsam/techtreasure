from django.urls import path
from login import  views


urlpatterns = [
    path('userprofile/setting/change_password', views.change_password, name='change_password'),
    path('userprofile/history/', views.history_views, name='history'),
    path('userprofile/get_history/', views.history_data, name='get_history'),
    path('makelisting/', views.make_listing, name='makelisting'),
]
