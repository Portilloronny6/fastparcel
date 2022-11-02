from rest_framework import serializers

from shipping.models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ['photo', 'pickup_photo', 'delivery_photo']
