import firebase_admin
import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from firebase_admin import credentials, auth

from shipping.forms import BasicUserForm, BasicCustomerForm, CustomPasswordResetForm, JobStep1Form

cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)

stripe.api_key = settings.STRIPE_API_SECRET_KEY


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
            return redirect(reverse('customer:profile_page'))

        password_form = CustomPasswordResetForm(request.user, request.POST)
        if request.POST.get('reset_form') and password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, 'Your password has been updated.')
            return redirect(reverse('customer:profile_page'))

        if request.POST.get('phone_check'):
            try:
                firebase_user = auth.verify_id_token(request.POST.get('id_token', ''))
                request.user.customer.phone_number = firebase_user.get('phone_number', '')
                request.user.customer.save()
                messages.success(request, 'Your phone number has been approved.')
                return redirect(reverse('customer:profile_page'))
            except:
                messages.error(request, 'A problem has occurred')
                return redirect(reverse('customer:profile_page'))

        context = {
            'user_form': BasicUserForm(instance=request.user),
            'customer_form': BasicCustomerForm(instance=request.user.customer),
            'password_form': password_form,
        }
        return render(request, 'customers/profile.html', context)


class PaymentMethodView(LoginRequiredMixin, View):
    login_url = '/sign-in/?next=/customer/'

    def get(self, request):
        current_customer = request.user.customer
        if not current_customer.stripe_customer_id:
            customer = stripe.Customer.create()
            current_customer.stripe_customer_id = customer.get('id', '')
            current_customer.save()

        stripe_payment_methods = stripe.Customer.list_payment_methods(
            current_customer.stripe_customer_id,
            type='card',
        )
        if stripe_payment_methods and stripe_payment_methods.data:
            current_customer.stripe_payment_method_id = stripe_payment_methods.data[0].id
            current_customer.stripe_card_last4 = stripe_payment_methods.data[0].card.last4
            current_customer.save()
        else:
            current_customer.stripe_payment_method_id = ''
            current_customer.stripe_card_last4 = ''
            current_customer.save()

        if not current_customer.stripe_payment_method_id:
            intent = stripe.SetupIntent.create(
                customer=current_customer.stripe_customer_id,
                payment_method_types=['card'],
            )

            context = {
                'client_secret': intent.client_secret,
                'STRIPE_API_PUBLIC_KEY': settings.STRIPE_API_PUBLIC_KEY,
            }
            return render(request, 'customers/payment_method.html', context)
        return render(request, 'customers/payment_method.html')

    def post(self, request):
        current_customer = request.user.customer
        stripe.PaymentMethod.detach(current_customer.stripe_payment_method_id)
        current_customer.stripe_card_last4 = ''
        current_customer.stripe_payment_method_id = ''
        current_customer.save()
        messages.success(request, 'Your payment method has been removed.')
        return redirect(reverse('customer:payment_method'))


class CreateJobView(LoginRequiredMixin, View):
    login_url = '/sign-in/?next=/customer/'

    def get(self, request):
        if not request.user.customer.stripe_payment_method_id:
            return redirect(reverse('customer:payment_method'))

        if not request.user.customer.phone_number:
            messages.warning(request, 'Please verify your phone number.')
            return redirect(reverse('customer:profile_page'))

        step1_form = JobStep1Form()
        context = {
            'step1_form': step1_form,
        }
        return render(request, 'customers/create_job.html', context)

    def post(self, request):
        return render(request, 'customers/create_job.html')
