from django.db import models
from django.core.validators import MinValueValidator


class Officer(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to="officers/", blank=True, null=True)

    display_order = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)] # no values <1 allowed
    )

    def __str__(self):
        return f"{self.name} - {self.role} - {self.display_order}"

    class Meta:
        ordering = ["display_order", "name"]



class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.date})"
