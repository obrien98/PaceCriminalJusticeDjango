from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import ContactMessage


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    CONTACT_RECIPIENT_EMAIL="club@example.com",
    DEFAULT_FROM_EMAIL="no-reply@example.com",
)
class ContactFormTests(TestCase):
    def test_homepage_renders_contact_form(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contact The Club")
        self.assertContains(response, 'name="email"', html=False)

    def test_valid_contact_submission_saves_message_and_sends_email(self):
        response = self.client.post(
            reverse("index"),
            data={
                "name": "Jordan Smith",
                "email": "jordan@example.com",
                "subject": "Joining the club",
                "message": "I would like to learn more about upcoming meetings.",
            },
            follow=True,
        )

        self.assertRedirects(response, f"{reverse('index')}?message=sent")
        self.assertEqual(ContactMessage.objects.count(), 1)

        contact_message = ContactMessage.objects.get()
        self.assertEqual(contact_message.name, "Jordan Smith")
        self.assertEqual(contact_message.subject, "Joining the club")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["club@example.com"])
        self.assertIn("Jordan Smith", mail.outbox[0].body)
        self.assertContains(response, 'class="page-alert page-alert-success"', html=False)
        self.assertContains(
            response,
            "Thanks for reaching out. Your message has been sent to the club.",
        )
