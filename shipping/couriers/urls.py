from django.urls import path

from shipping.couriers.views import CourierPageView

urlpatterns = [
    path('', CourierPageView.as_view(), name='courier_page'),
]
