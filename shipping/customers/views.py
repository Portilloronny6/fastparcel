from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from shipping.forms import BasicUserForm, BasicCustomerForm


class CustomerPageView(LoginRequiredMixin, View):

    def get(self, request):
        return redirect(reverse('profile_page'))


class ProfilePage(LoginRequiredMixin, View):
    login_url = '/sign_in/?next=/customer/'

    def get(self, request):
        user_form = BasicUserForm(instance=request.user)
        customer_form = BasicCustomerForm(instance=request.user.customer)
        password_form = PasswordChangeForm(request.user)

        context = {
            'user_form': user_form,
            'customer_form': customer_form,
            'password_form': password_form,
        }
        return render(request, 'customers/profile.html', context)

    def post(self, request):
        user_form = BasicUserForm(request.POST, instance=request.user)
        customer_form = BasicCustomerForm(request.POST, request.FILES, instance=request.user.customer)

        if request.POST.get('basic_form') and user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect(reverse('profile_page'))

        password_form = PasswordChangeForm(request.user, request.POST)
        if request.POST.get('reset_form') and password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'Your password has been updated.')
            return redirect(reverse('profile_page'))

        context = {
            'user_form': BasicUserForm(instance=request.user),
            'customer_form': BasicCustomerForm(instance=request.user.customer),
            'password_form': password_form,
        }
        return render(request, 'customers/profile.html', context)
