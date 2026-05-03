from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.templatetags.static import static
from django.test import TestCase, override_settings
from django.urls import reverse
from unittest.mock import patch
from datetime import date, time

from .models import ContactMessage, Event, GalleryImage, Officer


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
        self.assertContains(response, 'name="first_name"', html=False)
        self.assertContains(response, 'name="last_name"', html=False)
        self.assertContains(response, 'name="email"', html=False)

    def test_valid_contact_submission_saves_message_and_sends_email(self):
        response = self.client.post(
            reverse("index"),
            data={
                "first_name": "Jordan",
                "last_name": "Smith",
                "email": "jordan@example.com",
                "subject": "Joining the club",
                "message": "I would like to learn more about upcoming meetings.",
            },
            follow=True,
        )

        self.assertRedirects(response, f"{reverse('index')}?message=sent")
        self.assertEqual(ContactMessage.objects.count(), 1)

        contact_message = ContactMessage.objects.get()
        self.assertEqual(contact_message.first_name, "Jordan")
        self.assertEqual(contact_message.last_name, "Smith")
        self.assertEqual(contact_message.subject, "Joining the club")

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["club@example.com"])
        self.assertIn("First Name: Jordan", mail.outbox[0].body)
        self.assertIn("Last Name: Smith", mail.outbox[0].body)
        self.assertContains(response, 'class="page-alert page-alert-success"', html=False)
        self.assertContains(
            response,
            "Thanks for reaching out, Jordan! Your message has been sent to the club.",
        )

    @patch("core.views.send_mail", side_effect=Exception("SMTP failure"))
    def test_contact_submission_still_saves_when_email_send_fails(self, mocked_send_mail):
        response = self.client.post(
            reverse("index"),
            data={
                "first_name": "Jordan",
                "last_name": "Smith",
                "email": "jordan@example.com",
                "subject": "Joining the club",
                "message": "I would like to learn more about upcoming meetings.",
            },
            follow=True,
        )

        self.assertRedirects(response, f"{reverse('index')}?message=sent")
        self.assertEqual(ContactMessage.objects.count(), 1)
        mocked_send_mail.assert_called_once()
        self.assertContains(
            response,
            "Your message was saved, but the email notification could not be sent right now.",
        )


class OfficerImageTests(TestCase):
    def test_officer_uses_default_image_url_when_no_upload_exists(self):
        officer = Officer.objects.create(name="Alex Carter", role="President")

        self.assertEqual(officer.image_url, static("core/images/default.avif"))

    def test_homepage_renders_default_image_for_officer_without_upload(self):
        Officer.objects.create(name="Alex Carter", role="President")

        response = self.client.get(reverse("index"))

        self.assertContains(response, static("core/images/default.avif"))


class GalleryImageTests(TestCase):
    def test_homepage_uses_static_gallery_placeholders_when_no_admin_images_exist(self):
        response = self.client.get(reverse("index"))

        self.assertContains(response, static("core/images/img1.png"))

    def test_homepage_renders_gallery_images_from_database(self):
        uploaded_image = SimpleUploadedFile(
            "gallery-test.gif",
            (
                b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
                b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00"
                b"\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01"
                b"\x00;"
            ),
            content_type="image/gif",
        )
        gallery_image = GalleryImage.objects.create(
            title="Club Meeting",
            alt_text="Students at a club meeting",
            image=uploaded_image,
        )

        response = self.client.get(reverse("index"))

        self.assertContains(response, gallery_image.image.url)
        self.assertContains(response, "Students at a club meeting")

    def test_homepage_shows_only_featured_gallery_images(self):
        featured_image = GalleryImage.objects.create(
            title="Featured Photo",
            alt_text="Featured",
            is_featured=True,
            image=SimpleUploadedFile(
                "featured.gif",
                (
                    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
                    b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00"
                    b"\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01"
                    b"\x00;"
                ),
                content_type="image/gif",
            ),
        )
        non_featured_image = GalleryImage.objects.create(
            title="Archive Photo",
            alt_text="Archive",
            is_featured=False,
            image=SimpleUploadedFile(
                "archive.gif",
                (
                    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
                    b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00"
                    b"\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01"
                    b"\x00;"
                ),
                content_type="image/gif",
            ),
        )

        response = self.client.get(reverse("index"))

        self.assertContains(response, featured_image.image.url)
        self.assertNotContains(response, non_featured_image.image.url)

    def test_full_gallery_page_shows_all_gallery_images(self):
        first_image = GalleryImage.objects.create(
            title="Featured Photo",
            alt_text="Featured",
            is_featured=True,
            image=SimpleUploadedFile(
                "featured-two.gif",
                (
                    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
                    b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00"
                    b"\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01"
                    b"\x00;"
                ),
                content_type="image/gif",
            ),
        )
        second_image = GalleryImage.objects.create(
            title="Archive Photo",
            alt_text="Archive",
            is_featured=False,
            image=SimpleUploadedFile(
                "archive-two.gif",
                (
                    b"GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00"
                    b"\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00"
                    b"\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01"
                    b"\x00;"
                ),
                content_type="image/gif",
            ),
        )

        response = self.client.get(reverse("gallery_list"))

        self.assertContains(response, first_image.image.url)
        self.assertContains(response, second_image.image.url)


class EventTests(TestCase):
    def test_homepage_limits_events_and_links_to_full_event_page(self):
        for index in range(4):
            Event.objects.create(
                name=f"Event {index + 1}",
                date=date(2026, 5, index + 1),
                time=time(12, 0),
                location="Miller Hall",
            )

        response = self.client.get(reverse("index"))

        self.assertContains(response, "View All Events")
        self.assertContains(response, "Event 1")
        self.assertContains(response, "Event 2")
        self.assertContains(response, "Event 3")
        self.assertNotContains(response, "Event 4")

    def test_full_event_page_shows_all_events(self):
        first_event = Event.objects.create(
            name="Event 1",
            date=date(2026, 5, 1),
            time=time(12, 0),
            location="Miller Hall",
        )
        second_event = Event.objects.create(
            name="Event 2",
            date=date(2026, 5, 2),
            time=time(12, 0),
            location="Miller Hall",
        )

        response = self.client.get(reverse("event_list"))

        self.assertContains(response, first_event.name)
        self.assertContains(response, second_event.name)
