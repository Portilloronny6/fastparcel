from django.urls import path

from shipping.customers.views import *

app_name = 'customer'

urlpatterns = [
    path('profile/', ProfilePage.as_view(), name='profile_page'),
    path('profile/payment-method/', PaymentMethodView.as_view(), name='payment_method'),
    path('create-job/', CreateJobView.as_view(), name='create_job'),
    path('jobs/current/', CurrentJobView.as_view(), name='current_job'),
    path('jobs/archived/', ArchivedJobView.as_view(), name='archived_job'),
    path('jobs/<uuid:job_id>', JobDetailView.as_view(), name='job'),
]
