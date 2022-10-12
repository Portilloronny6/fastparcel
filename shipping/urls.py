from django.urls import path

from shipping.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
]
