import uuid

from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='customers/avatars/%d-%m-%Y/', blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True)
    stripe_payment_method_id = models.CharField(max_length=255, blank=True)
    stripe_card_last4 = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name()


class Job(models.Model):
    class Status(models.TextChoices):
        CREATED = 'created', 'Created'
        RECEIVED = 'received', 'Received'
        PROCESSING = 'processing', 'Processing'
        PICKING = 'picking', 'Picking'
        DELIVERING = 'delivering', 'Delivering'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        POSTPONED = 'postponed', 'Postponed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    photo = models.ImageField(upload_to='jobs/photos/%d-%m-%Y/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    pickup_address = models.CharField(max_length=255, blank=True)
    pickup_lat = models.FloatField(default=0.0)
    pickup_lng = models.FloatField(default=0.0)
    pickup_name = models.CharField(max_length=255, blank=True)
    pickup_phone = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name
