from django.urls import path

from shipping.customers.views import *

urlpatterns = [
    path('', CustomerPageView.as_view(), name='customer_page'),
    path('profile', ProfilePage.as_view(), name='profile_page'),
]
