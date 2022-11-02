from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from fastparcel.settings import GOOGLE_MAPS_CREDENTIAL


class AvailableJobsView(LoginRequiredMixin, View):
    login_url = '/sign-in/?next=/courier/'

    def get(self, request):
        context = {
            "GOOGLE_MAPS_CREDENTIAL": GOOGLE_MAPS_CREDENTIAL,
        }
        return render(request, 'couriers/available_jobs.html', context=context)