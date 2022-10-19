from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from shipping.models import Customer, Job


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=250)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address already exists.')
        return email


class BasicUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')


class BasicCustomerForm(forms.ModelForm):
    avatar = forms.FileField(widget=forms.FileInput)

    class Meta:
        model = Customer
        fields = ('avatar',)


class CustomPasswordResetForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': False}),
    )


class JobCreateForm(forms.ModelForm):
    photo = forms.ImageField(required=True)

    class Meta:
        model = Job
        fields = ('name', 'description', 'quantity', 'photo')


class JobPickUpForm(forms.ModelForm):
    pickup_address = forms.CharField(required=True)
    pickup_name = forms.CharField(required=True)
    pickup_phone = forms.CharField(required=True)
    pickup_lat = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    pickup_lng = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Job
        fields = ('pickup_address', 'pickup_lat', 'pickup_lng', 'pickup_name', 'pickup_phone')


class JobDeliveryForm(forms.ModelForm):
    delivery_address = forms.CharField(required=True)
    delivery_name = forms.CharField(required=True)
    delivery_phone = forms.CharField(required=True)
    delivery_lat = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    delivery_lng = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))

    class Meta:
        model = Job
        fields = ('delivery_address', 'delivery_lat', 'delivery_lng', 'delivery_name', 'delivery_phone')
