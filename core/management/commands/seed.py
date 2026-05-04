from django.core.management.base import BaseCommand
from datetime import date, time
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from urllib.parse import urlparse
from urllib.request import urlopen
import os

from core.models import Event, GalleryImage, Officer


class Command(BaseCommand):
    help = "Seed database with initial data"

    def _static_images_path(self):
        return os.path.join(
            settings.BASE_DIR,
            "core",
            "static",
            "core",
            "images",
        )

    def _attach_local_image(self, instance, field_name, image_name):
        image_path = os.path.join(self._static_images_path(), image_name)
        if not os.path.exists(image_path):
            self.stdout.write(
                self.style.WARNING(f"Skipped missing seed image: {image_name}")
            )
            return

        with open(image_path, "rb") as image_file:
            getattr(instance, field_name).save(
                image_name,
                File(image_file),
                save=True,
            )

    def _attach_remote_image(self, instance, field_name, image_url, fallback_name):
        parsed_url = urlparse(image_url)
        filename = os.path.basename(parsed_url.path) or fallback_name

        with urlopen(image_url) as response:
            image_bytes = response.read()

        getattr(instance, field_name).save(
            filename,
            ContentFile(image_bytes),
            save=True,
        )

    def _seed_gallery_from_urls(self, gallery_items):
        for index, gallery_item in enumerate(gallery_items, start=1):
            image_url = gallery_item["image_url"]
            gallery_image = GalleryImage(
                title=gallery_item.get("title", f"Gallery Image {index}"),
                alt_text=gallery_item.get("alt_text", f"CJS event photo {index}"),
                is_featured=gallery_item.get("is_featured", False),
                display_order=gallery_item.get("display_order", index),
            )
            self._attach_remote_image(
                gallery_image,
                "image",
                image_url,
                f"gallery-image-{index}.jpg",
            )
            self.stdout.write(f"Created gallery image {index} from {image_url}")

    def _seed_gallery_from_static_files(self):
        gallery_items = [
            {
                "title": "Meeting with the Bureau of Alcohol, Tobacco and Firearms",
                "alt_text": "Meeting with the Bureau of Alcohol, Tobacco and Firearms",
                "image_name": "img1.png",
                "display_order": 1,
                "is_featured": True,
            },
            {
                "title": "The Club at a Drunk Driving Simulator",
                "alt_text": "The Club at a Drunk Driving Simulator",
                "image_name": "img2.png",
                "display_order": 2,
                "is_featured": True,
            },
            {
                "title": "We got to meet the K9!",
                "alt_text": "Club with k9 dog",
                "image_name": "img3.png",
                "display_order": 3,
                "is_featured": True,
            },
            {
                "title": "Self Defense Keychains",
                "alt_text": "Self Defense Keychains",
                "image_name": "img4.png",
                "display_order": 4,
                "is_featured": True,
            },
            {
                "title": "Winning awards!",
                "alt_text": "Outstanding Advocacy Certificate",
                "image_name": "img6.png",
                "display_order": 5,
            },
            {
                "title": "CJS Event Photo 5",
                "alt_text": "Criminal Justice Society event photo 5",
                "image_name": "img5.png",
                "display_order": 6,
            },
            {
                "title": "CJS Event Photo 7",
                "alt_text": "Criminal Justice Society event photo 7",
                "image_name": "img7.png",
                "display_order": 7,
            },
            {
                "title": "CJS Event Photo 8",
                "alt_text": "Criminal Justice Society event photo 8",
                "image_name": "img8.png",
                "display_order": 8,
            },
        ]

        for index, gallery_item in enumerate(gallery_items, start=1):
            image_name = gallery_item["image_name"]
            gallery_image = GalleryImage(
                title=gallery_item.get("title", f"Gallery Image {index}"),
                alt_text=gallery_item.get("alt_text", f"CJS event photo {index}"),
                is_featured=gallery_item.get("is_featured", False),
                display_order=gallery_item.get("display_order", index),
            )
            self._attach_local_image(gallery_image, "image", image_name)
            self.stdout.write(f"Created gallery image {index}: {image_name}")

    def handle(self, *args, **kwargs):
        # Clear existing data (optional)
        Officer.objects.all().delete()
        Event.objects.all().delete()
        GalleryImage.objects.all().delete()

        # -------- OFFICERS --------
        officers = [
            {
                "name": "Natasha DePaoli",
                "role": "President",
                "email": "nd78713@pace.edu", 
                "bio": "Leads the overall vision of the Criminal Justice Society, coordinating events, guiding strategy, and representing the organization across campus.",
                "display_order": 1,
            },
            {
                "name": "Toni Ramunno",
                "role": "Vice President",
                "email": "tr69175p@pace.edu", 
                "bio": "Supports event coordination, member engagement, and overall club operations while helping ensure everything runs smoothly.",
                "linkedIn": "reidhoffman",
                "display_order": 2,
            },
            {
                "name": "Emma Seijo",
                "role": "Officer",
                "email": "es96754p@pace.edu", 
                "bio": "Assists with events, programming, and member engagement while contributing to a positive and inclusive club environment.",
                "display_order": 3,
            },
            {
                "name": "Yamilet Ulerio",
                "role": "Treasurer",
                "email": "yu62771p@pace.edu", 
                "bio": "Manages budgeting and finances, ensuring responsible use of funds for events and student initiatives.",
                "linkedIn": "reidhoffman",
                "instagram": "paceplv.cjs",
                "display_order": 4,
            },
            {
                "name": "Leah Ayala",
                "role": "Senator",
                "email": "la03172@pace.edu", 
                "bio": "Represents the club in student government and helps connect the organization with campus leadership and resources.",
                "display_order": 5,
            },
            {
                "name": "Ciara Chenault",
                "role": "Secretary",
                "email": "cc79402@pace.edu", 
                "bio": "Keeps records of meetings and communications, helping the organization stay organized and efficient.",
                "display_order": 6,
            },
        ]

        for officer in officers:
            Officer.objects.create(**officer)

        # -------- EVENTS --------
        events = [
            {
                "name": "Trivia Night",
                "date": date(2026, 4, 28),
                "time": time(12, 10),
                "location": "KESSEL MULTIPURPOSE ROOM, ROOM 206",
                "description": "Join the Criminal Justice Society for a night of trivia!\n We will have Wingstop, Prizes, Giveaways and more!.",
                "image_name": "trivia-night.png",
            },
            {
                "name": "Relay For Life",
                "date": date(2026, 3, 18),
                "time": time(12, 10),
                "location": "Miller Hall 22, Active Learning Classroom",
                "description": "Come join us for a 12 hour walkathon to raise money and awareness for cancer! There will be raffles, prizes, inflatables and catered food! Participate in our games, activity tables or walkathon!",
                "image_name": "relay-for-life.png",
            },
            {
                "name": "Self Defense Training with the Mount Pleasant Police Department",
                "date": date(2026, 3, 18),
                "time": time(12, 10),
                "location": "Miller Hall 22, Active Learning Classroom",
                "description": "The Mount Pleasant Police Department will be hosting a hands on self defense class. Learn how to defend yourself while enjoying raffles, giveaways, food and more!",
                "image_name": "self-defense.png",
            },
            {
                "name": "Pace Law School Mock Trial",
                "date": date(2026, 3, 18),
                "time": time(12, 10),
                "location": "Miller Hall 22, Active Learning Classroom",
                "description": "The Criminal Justice Society will be visiting Pace Law School in White Plains for a joint event. This year, students will have the opportunity to participate in a mock trial in addition to the law school tour.\nStudents are needed to fill the following roles: two for the prosecution, two for the defense, and six jurors. All students planning to attend must be available to meet at least once online with Professor Dorfman prior to the visit. \nIf you are interested in attending or have any questions, please email me at nd78713p@pace.edu ",
                "image_name": "mock-trial.png",
            },
            {
                "name": "Crime Scene Investigation",
                "date": date(2026, 3, 18),
                "time": time(12, 10),
                "location": "Miller Hall 22, Active Learning Classroom",
                "description": "Interested in the investigative process. Here from a criminal investigator with the White Plains Department of Public Safety!",
                "image_name": "csi.png",
            },
        ]

        for event_data in events:
            image_name = event_data.pop("image_name", None)
            image_url = event_data.pop("image_url", None)
            event = Event.objects.create(**event_data)

            if image_url:
                self._attach_remote_image(
                    event,
                    "image",
                    image_url,
                    f"{event.name.lower().replace(' ', '-')}.jpg",
                )
            elif image_name:
                self._attach_local_image(event, "image", image_name)

        
        # -------- GALLERY IMAGES --------
        gallery_urls = [
            image_url.strip()
            for image_url in os.getenv("CLOUDINARY_GALLERY_SEED_URLS", "").splitlines()
            if image_url.strip()
        ]

        gallery_items = [
            {
                "title": f"CJS Event Photo {index}",
                "alt_text": f"Criminal Justice Society event photo {index}",
                "image_url": image_url,
                "display_order": index,
                "is_featured": index <= 4,
            }
            for index, image_url in enumerate(gallery_urls, start=1)
        ]

        if gallery_items:
            self._seed_gallery_from_urls(gallery_items)
        else:
            self._seed_gallery_from_static_files()

        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))
