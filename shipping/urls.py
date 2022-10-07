from django.urls import path

from shipping.views import home

urlpatterns = [
    path('', home, name='home'),
]
