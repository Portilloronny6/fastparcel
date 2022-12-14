from django.urls import path, include
from django.contrib.auth import views as auth_views

from shipping.views import HomeView, SignUpView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    path('sign-in/', auth_views.LoginView.as_view(template_name='sign_in.html'), name='sign_in'),
    path('sign-out/', auth_views.LogoutView.as_view(next_page='/'), name='sign_out'),
    path('sign-up/', SignUpView.as_view(), name='sign_up'),

    path('customer/', include('shipping.customers.urls')),
    path('courier/', include('shipping.couriers.urls')),
]
