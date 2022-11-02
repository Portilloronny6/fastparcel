from django.urls import path

from shipping.couriers.api_views import AvailableJobsApiView
from shipping.couriers.views import AvailableJobsView

app_name = 'courier'

urlpatterns = [
    path('jobs/available/', AvailableJobsView.as_view(), name='available_jobs'),

    path('api/jobs/available/', AvailableJobsApiView.as_view(), name='available_jobs_api'),
]
