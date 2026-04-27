from django.db import models
from django.core.validators import MinValueValidator
from django.templatetags.static import static


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

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return static("core/images/default.avif")

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


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.subject} - {self.name}"


class GalleryImage(models.Model):
    title = models.CharField(max_length=150)
    image = models.ImageField(upload_to="gallery/")
    alt_text = models.CharField(max_length=200, blank=True)
    is_featured = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order", "id"]

    def __str__(self):
        return self.title

    @property
    def accessible_alt_text(self):
        return self.alt_text or self.title
