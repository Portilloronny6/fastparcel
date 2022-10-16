import firebase_admin
import requests
import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from firebase_admin import credentials, auth

from shipping.forms import BasicUserForm, BasicCustomerForm, \
    CustomPasswordResetForm, JobCreateForm, JobPickUpForm, JobDeliveryForm
from shipping.models import Job, Transaction

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
        current_customer = request.user.customer
        if not current_customer.stripe_payment_method_id:
            return redirect(reverse('customer:payment_method'))

        if not current_customer.phone_number:
            messages.warning(request, 'Please verify your phone number.')
            return redirect(reverse('customer:profile_page'))

        job = Job.objects.filter(customer=current_customer, status=Job.Status.CREATED).last()
        created_form = JobCreateForm(instance=job)
        pickup_form = JobPickUpForm(instance=job)
        delivery_form = JobDeliveryForm(instance=job)

        # Determine which step we are
        if not job:
            current_step = Job.Steps.CREATED
        elif job.delivery_name:
            current_step = Job.Steps.COMPLETED
        elif job.pickup_name:
            current_step = Job.Steps.DELIVERY
        else:
            current_step = Job.Steps.PICKUP

        context = {
            'created_form': created_form,
            'pickup_form': pickup_form,
            'delivery_form': delivery_form,
            'job': job,
            'steps': Job.Steps,
            'current_step': current_step,
            'GOOGLE_MAPS_CREDENTIAL': settings.GOOGLE_MAPS_CREDENTIAL,
        }
        return render(request, 'customers/create_job.html', context)

    def post(self, request):
        current_customer = request.user.customer
        job = Job.objects.filter(customer=current_customer, status=Job.Status.CREATED).last()
        if request.POST.get('step') == Job.Status.CREATED:
            created_form = JobCreateForm(request.POST, request.FILES, instance=job)

            if created_form.is_valid():
                creating_job = created_form.save(commit=False)
                creating_job.customer = current_customer
                creating_job.save()
                return redirect(reverse('customer:create_job'))

        elif request.POST.get('step') == Job.Status.PICKING:
            pickup_form = JobPickUpForm(request.POST, instance=job)
            if not pickup_form.is_valid() or not job:
                messages.error(request, 'Previous step is not completed.')
                return redirect(reverse('customer:create_job'))
            pickup_form.save()
            return redirect(reverse('customer:create_job'))

        elif request.POST.get('step') == Job.Status.DELIVERING:
            delivery_form = JobDeliveryForm(request.POST, instance=job)
            if not delivery_form.is_valid() or not job or not job.pickup_name:
                messages.error(request, 'Previous step is not completed.')
                return redirect(reverse('customer:create_job'))

            try:
                response = requests.get(
                    "https://maps.googleapis.com/maps/api/distancematrix/json?&origins={},{}&destinations={},{}&key={}".format(
                        job.pickup_lat,
                        job.pickup_lng,
                        job.delivery_lat,
                        job.delivery_lng,
                        settings.GOOGLE_MAPS_CREDENTIAL,
                    ))
                if response.json().get('status', '') == 'OK':
                    r = response.json()
                    job.distance = round(r.get('rows')[0].get('elements')[0].get('distance').get('value') / 1000, 2)
                    job.duration = int(r.get('rows')[0].get('elements')[0].get('duration').get('value') / 60)
                    job.price = round(job.distance * 0.8, 2)  # $0.8 per km
                    job.save()
                    delivery_form.save()
                    return redirect(reverse('customer:create_job'))
            except Exception:
                messages.error(request, 'Unfortunately, we do not support shipping to this address.')
                return redirect(reverse('customer:create_job'))

        elif request.POST.get('step') == Job.Status.COMPLETED:
            if not job or not job.pickup_name or not job.delivery_name:
                messages.error(request, 'Previous step is not completed.')
                return redirect(reverse('customer:create_job'))
            try:
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(job.price * 100),
                    currency='usd',
                    customer=request.user.customer.stripe_customer_id,
                    payment_method=request.user.customer.stripe_payment_method_id,
                    off_session=True,
                    confirm=True,
                )
                Transaction.objects.create(
                    stripe_payment_intent_id=payment_intent.get('id'),
                    job=job,
                    amount=job.price,
                )
                job.status = Job.Status.PROCESSING
                job.save()

                messages.success(request, 'Your payment has been processed successfully.')
                return redirect(reverse('customer:profile_page'))
            except stripe.error.CardError as e:
                err = e.error
                # Error code will be authentication_required if authentication is needed
                print("Code is: %s" % err.code)
                payment_intent_id = err.payment_intent['id']
                payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
                messages.error(request, 'Your card was declined.')
                return redirect(reverse('customer:profile_page'))
