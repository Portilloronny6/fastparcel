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
    class Steps:
        CREATED = 1
        PICKUP = 2
        DELIVERY = 3
        COMPLETED = 4

    class Status(models.TextChoices):
        CREATED = 'created', 'Created'
        RECEIVED = 'received', 'Received'
        PROCESSING = 'processing', 'Processing'
        PICKING = 'picking', 'Picking'
        DELIVERING = 'delivering', 'Delivering'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'
        POSTPONED = 'postponed', 'Postponed'

    # Order Info Step
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    photo = models.ImageField(upload_to='jobs/photos/%d-%m-%Y/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.CREATED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Picking Step
    pickup_address = models.CharField(max_length=255, blank=True)
    pickup_lat = models.FloatField(default=0.0)
    pickup_lng = models.FloatField(default=0.0)
    pickup_name = models.CharField(max_length=255, blank=True)
    pickup_phone = models.CharField(max_length=255, blank=True)

    # Delivering Step
    delivery_address = models.CharField(max_length=255, blank=True)
    delivery_lat = models.FloatField(default=0.0)
    delivery_lng = models.FloatField(default=0.0)
    delivery_name = models.CharField(max_length=255, blank=True)
    delivery_phone = models.CharField(max_length=255, blank=True)

    # Completed Step
    duration = models.IntegerField(default=0)
    distance = models.FloatField(default=0.0)
    price = models.FloatField(default=0.0)

    # Detail
    pickup_photo = models.ImageField(upload_to='jobs/pickup/%d-%m-%Y/', blank=True, null=True)
    pickedup_at = models.DateTimeField(blank=True, null=True)

    delivery_photo = models.ImageField(upload_to='jobs/delivery/%d-%m-%Y/', blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class Transaction(models.Model):
    stripe_payment_intent_id = models.CharField(max_length=255, unique=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    amount = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stripe_payment_intent_id
