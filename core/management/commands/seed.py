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

    def _seed_gallery_from_urls(self, image_urls):
        for index, image_url in enumerate(image_urls, start=1):
            parsed_url = urlparse(image_url)
            filename = os.path.basename(parsed_url.path) or f"gallery-image-{index}.jpg"

            with urlopen(image_url) as response:
                image_bytes = response.read()

            gallery_image = GalleryImage(
                title=f"Gallery Image {index}",
                alt_text=f"CJS event photo {index}",
                display_order=index,
            )
            gallery_image.image.save(filename, ContentFile(image_bytes), save=True)
            self.stdout.write(f"Created gallery image {index} from {image_url}")

    def _seed_gallery_from_static_files(self):
        image_names = ["img1.png", "img2.png", "img3.png", "img4.png", "img5.png", "img6.png", "img7.png", "img8.png"]
        static_images_path = os.path.join(
            settings.BASE_DIR,
            "core",
            "static",
            "core",
            "images",
        )

        for index, image_name in enumerate(image_names, start=1):
            image_path = os.path.join(static_images_path, image_name)
            if not os.path.exists(image_path):
                self.stdout.write(
                    self.style.WARNING(f"Skipped missing gallery seed image: {image_name}")
                )
                continue

            with open(image_path, "rb") as image_file:
                gallery_image = GalleryImage(
                    title=f"Gallery Image {index}",
                    alt_text=f"CJS event photo {index}",
                    display_order=index,
                )
                gallery_image.image.save(
                    image_name,
                    File(image_file),
                    save=True,
                )
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
        Event.objects.create(
            name="Crime Scene Investigation",
            date=date(2026, 3, 18),
            time=time(12, 10),
            location="Miller Hall 22, Active Learning Classroom",
            description="Hear from a criminal investigator with the White Plains Department of Public Safety about the investigative process.",
        )
        Event.objects.create(
            name="Trivia Night",
            date=date(2026, 4, 28),
            time=time(12, 10),
            location="KESSEL MULTIPURPOSE ROOM, ROOM 206",
            description="Join the Criminal Justice Society for a night of trivia!\n We will have Wingstop, Prizes, Giveaways and more!.",
        )
        Event.objects.create(
            name="Relay For Life",
            date=date(2026, 3, 18),
            time=time(12, 10),
            location="Miller Hall 22, Active Learning Classroom",
            description="Come join us for a 12 hour walkathon to raise money and awareness for cancer! There will be raffles, prizes, inflatables and catered food! Participate in our games, activity tables or walkathon!",
        )
        Event.objects.create(
            name="Trivia Night",
            date=date(2026, 4, 28),
            time=time(12, 10),
            location="KESSEL MULTIPURPOSE ROOM, ROOM 206",
            description="Join the Criminal Justice Society for a night of trivia!\n We will have Wingstop, Prizes, Giveaways and more!.",
        )
        Event.objects.create(
            name="Pace Law School Mock Trial",
            date=date(2026, 3, 18),
            time=time(12, 10),
            location="Miller Hall 22, Active Learning Classroom",
            description="The Criminal Justice Society will be visiting Pace Law School in White Plains for a joint event. This year, students will have the opportunity to participate in a mock trial in addition to the law school tour.\nStudents are needed to fill the following roles: two for the prosecution, two for the defense, and six jurors. All students planning to attend must be available to meet at least once online with Professor Dorfman prior to the visit. \nIf you are interested in attending or have any questions, please email me at nd78713p@pace.edu ",
)
        Event.objects.create(
            name="Trivia Night",
            date=date(2026, 4, 28),
            time=time(12, 10),
            location="KESSEL MULTIPURPOSE ROOM, ROOM 206",
            description="Join the Criminal Justice Society for a night of trivia!\n We will have Wingstop, Prizes, Giveaways and more!.",
        )
        Event.objects.create(
        name="Crime Scene Investigation",
        date=date(2026, 3, 18),
        time=time(12, 10),
        location="Miller Hall 22, Active Learning Classroom",
        description="Hear from a criminal investigator with the White Plains Department of Public Safety about the investigative process.",
        )
        Event.objects.create(
            name="Trivia Night",
            date=date(2026, 4, 28),
            time=time(12, 10),
            location="KESSEL MULTIPURPOSE ROOM, ROOM 206",
            description="Join the Criminal Justice Society for a night of trivia!\n We will have Wingstop, Prizes, Giveaways and more!.",
        )
        Event.objects.create(
            name="Crime Scene Investigation",
            date=date(2026, 3, 18),
            time=time(12, 10),
            location="Miller Hall 22, Active Learning Classroom",
            description="Hear from a criminal investigator with the White Plains Department of Public Safety about the investigative process.",
        )
        Event.objects.create(
            name="Trivia Night",
            date=date(2026, 4, 28),
            time=time(12, 10),
            location="KESSEL MULTIPURPOSE ROOM, ROOM 206",
            description="Join the Criminal Justice Society for a night of trivia!\n We will have Wingstop, Prizes, Giveaways and more!.",
        )
        Event.objects.create(
        name="Crime Scene Investigation",
        date=date(2026, 3, 18),
        time=time(12, 10),
        location="Miller Hall 22, Active Learning Classroom",
        description="Hear from a criminal investigator with the White Plains Department of Public Safety about the investigative process.",
        )
        Event.objects.create(
            name="Trivia Night",
            date=date(2026, 4, 28),
            time=time(12, 10),
            location="KESSEL MULTIPURPOSE ROOM, ROOM 206",
            description="Join the Criminal Justice Society for a night of trivia!\n We will have Wingstop, Prizes, Giveaways and more!.",
        )
        

        # -------- GALLERY IMAGES --------
        image_urls = [
            image_url.strip()
            for image_url in os.getenv("CLOUDINARY_GALLERY_SEED_URLS", "").splitlines()
            if image_url.strip()
        ]

        if image_urls:
            self._seed_gallery_from_urls(image_urls)
        else:
            self._seed_gallery_from_static_files()

        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))
