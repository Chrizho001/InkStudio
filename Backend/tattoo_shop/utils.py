from django.core.mail import send_mail
from django.conf import settings

def booking_confirmation(author, author_email, booking):
    # Send an email to the user whenever a booking is made
    subject = f"Tattoo Session Order"
    message = f"Hello {author},\n\nYour tattoo session booking with Dark Ink on {booking.session_date} is being reviewed by the admins and you will be notified as soon as it is confirmed.\n\nThank you for using our service!"
    recipient_list = [author_email]

    # Send the email
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient_list,
        fail_silently=False,
    )
