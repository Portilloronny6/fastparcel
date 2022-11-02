from rest_framework.generics import ListAPIView

from shipping.couriers.serializers import JobSerializer
from shipping.models import Job


class AvailableJobsApiView(ListAPIView):
    serializer_class = JobSerializer

    def get_queryset(self):
        return Job.objects.filter(status=Job.Status.PROCESSING)
