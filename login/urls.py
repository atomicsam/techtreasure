from django.urls import path

from login.views import HistoryClassModel, ChangePasswordModel, MakeListingModel, GetHistoryClassModel

urlpatterns = [
    path('userprofile/setting/change_password', ChangePasswordModel.as_view(), name='change_password'),
    path('userprofile/history/', GetHistoryClassModel.as_view(), name='history'),
    path('userprofile/get_history/', HistoryClassModel.as_view(), name='get_history'),
    path('makelisting/', MakeListingModel.as_view(), name='makelisting'),
]
