from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View

from shipping.forms import SignUpForm


class SignUpView(View):

    def get(self, request):
        form = SignUpForm()
        context = {
            'form': form
        }
        return render(request, 'sign_up.html', context)

    def post(self, request):
        form = SignUpForm(request.POST)
        context = {
            'form': form,
        }
        if form.is_valid():
            email = form.cleaned_data.get('email', '')
            user = form.save(commit=False)
            user.username = email
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            redirect('sign_in')
        return render(request, 'home.html', context)


class HomeView(View):

    def get(self, request):
        return render(request, 'home.html')
