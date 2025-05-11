from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking


@receiver(post_save, sender=Booking)
def send_booking_status_email(sender, instance, created, **kwargs):
    # Check if the booking status has been updated (and not created)
    if not created and instance.status:
        # Send an email to the user whenever the status is updated
        subject = f"Your booking status has been updated!"
        message = f"Hello {instance.user.first_name},\n\nYour booking with {instance.artist.name} has been updated to {instance.status}.\n\nThank you for using our service!"
        recipient_list = [instance.user.email]

        # Send the email
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
