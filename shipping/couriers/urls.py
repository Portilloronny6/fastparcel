from django.urls import path

from shipping.couriers.views import AvailableJobsView

app_name = 'courier'

urlpatterns = [
    path('jobs/available/', AvailableJobsView.as_view(), name='available_jobs'),
]
