from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created and instance.email:
        subject = 'Welcome to FastParcel!'
        message = render_to_string('welcome_email.html', {'name': instance.get_full_name()})
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.email], fail_silently=False)
