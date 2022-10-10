from django.urls import path

from shipping.customers.views import *

app_name = 'customer'

urlpatterns = [
    path('profile/', ProfilePage.as_view(), name='profile_page'),
    path('profile/payment-method/', PaymentMethodView.as_view(), name='payment_method'),
    path('create-job/', CreateJobView.as_view(), name='create_job'),
]
