import firebase_admin
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from firebase_admin import credentials, auth

from shipping.forms import BasicUserForm, BasicCustomerForm, CustomPasswordResetForm

cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)


class CustomerPageView(LoginRequiredMixin, View):
    login_url = '/sign-in/?next=/customer/'

    def get(self, request):
        return redirect(reverse('profile_page'))


class ProfilePage(LoginRequiredMixin, View):
    login_url = '/sign-in/?next=/customer/'

    def get(self, request):
        user_form = BasicUserForm(instance=request.user)
        customer_form = BasicCustomerForm(instance=request.user.customer)
        password_form = CustomPasswordResetForm(request.user)

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

        password_form = CustomPasswordResetForm(request.user, request.POST)
        if request.POST.get('reset_form') and password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'Your password has been updated.')
            return redirect(reverse('profile_page'))

        if request.POST.get('phone_check'):
            try:
                firebase_user = auth.verify_id_token(request.POST.get('id_token', ''))
                request.user.customer.phone_number = firebase_user.get('phone_number', '')
                request.user.customer.save()
                return redirect(reverse('profile_page'))
            except:
                messages.error(request, 'A problem has occurred')
                return redirect(reverse('profile_page'))

        context = {
            'user_form': BasicUserForm(instance=request.user),
            'customer_form': BasicCustomerForm(instance=request.user.customer),
            'password_form': password_form,
        }
        return render(request, 'customers/profile.html', context)


class PaymentMethodView(LoginRequiredMixin, View):
    login_url = '/sign-in/?next=/customer/'

    def get(self, request):
        return render(request, 'customers/payment_method.html')

    def post(self, request):
        return redirect(reverse('profile_page'))
