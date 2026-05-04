from django.conf import settings
from django.core.mail import send_mail


def send_contact_notification(contact_message):
    plain_text_message = (
        f"First Name: {contact_message.first_name}\n"
        f"Last Name: {contact_message.last_name}\n"
        f"Email: {contact_message.email}\n\n"
        f"{contact_message.message}"
    )

    if getattr(settings, "SENDGRID_API_KEY", ""):
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail

        html_message = (
            f"<p><strong>First Name:</strong> {contact_message.first_name}</p>"
            f"<p><strong>Last Name:</strong> {contact_message.last_name}</p>"
            f"<p><strong>Email:</strong> {contact_message.email}</p>"
            f"<p><strong>Message:</strong></p>"
            f"<p>{contact_message.message}</p>"
        )

        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=settings.CONTACT_RECIPIENT_EMAIL,
            subject=f"CJS Contact Form: {contact_message.subject}",
            plain_text_content=plain_text_message,
            html_content=html_message,
        )
        SendGridAPIClient(settings.SENDGRID_API_KEY).send(message)
        return

    send_mail(
        subject=f"CJS Contact Form: {contact_message.subject}",
        message=plain_text_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
        fail_silently=False,
    )
