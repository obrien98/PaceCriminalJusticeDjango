from django.core.management.base import BaseCommand
from core.models import Officer, Event
from datetime import date, time


class Command(BaseCommand):
    help = "Seed database with initial data"

    def handle(self, *args, **kwargs):
        # Clear existing data (optional)
        Officer.objects.all().delete()
        Event.objects.all().delete()

        # -------- OFFICERS --------
        officers = [
            {
                "name": "Natasha DePaoli",
                "role": "President",
                "bio": "Leads the overall vision of the Criminal Justice Society, coordinating events, guiding strategy, and representing the organization across campus.",
                "display_order": 1,
            },
            {
                "name": "Toni Ramunno",
                "role": "Vice President",
                "bio": "Supports event coordination, member engagement, and overall club operations while helping ensure everything runs smoothly.",
                "display_order": 2,
            },
            {
                "name": "Emma Seijo",
                "role": "Officer",
                "bio": "Assists with events, programming, and member engagement while contributing to a positive and inclusive club environment.",
                "display_order": 3,
            },
            {
                "name": "Yamilet Ulerio",
                "role": "Treasurer",
                "bio": "Manages budgeting and finances, ensuring responsible use of funds for events and student initiatives.",
                "display_order": 4,
            },
            {
                "name": "Leah Ayala",
                "role": "Senator",
                "bio": "Represents the club in student government and helps connect the organization with campus leadership and resources.",
                "display_order": 5,
            },
            {
                "name": "Ciara Chenault",
                "role": "Secretary",
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

        self.stdout.write(self.style.SUCCESS("Database seeded successfully"))