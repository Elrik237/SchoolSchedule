from django.urls import path
from .views import *

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('search', SearchSchedule.as_view(), name='search'),
    path('delete-all', DeleteAll.as_view(), name='delete-all'),
] 
