from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ContactMessageForm
from .models import Event, GalleryImage, Officer

def index(request):
    leadership = Officer.objects.all()
    events = Event.objects.all()
    featured_gallery_images = list(GalleryImage.objects.filter(is_featured=True)[:6])
    if featured_gallery_images:
        gallery_images = featured_gallery_images
    else:
        gallery_images = list(GalleryImage.objects.all()[:6])
    has_full_gallery = GalleryImage.objects.count() > len(gallery_images)

    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            try:
                send_mail(
                    subject=f"CJS Contact Form: {contact_message.subject}",
                    message=(
                        f"Name: {contact_message.name}\n"
                        f"Email: {contact_message.email}\n\n"
                        f"{contact_message.message}"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                    fail_silently=False,
                )
                messages.success(
                    request,
                    "Thanks for reaching out. Your message has been sent to the club.",
                )
            except Exception as e:
                print("EMAIL ERROR:", str(e))  # 👈 this will show in Render logs
                raise e
            return redirect(f"{reverse('index')}?message=sent")
    else:
        form = ContactMessageForm()

    context = {
        'leadership': leadership,
        'events': events,
        "gallery_images": gallery_images,
        "has_full_gallery": has_full_gallery,
        "contact_form": form,
    }
    return render(request, "core/index.html", context)


def gallery_list(request):
    gallery_images = GalleryImage.objects.all()
    context = {
        "gallery_images": gallery_images,
    }
    return render(request, "core/gallery_list.html", context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    events = Event.objects.all()
    context = {
        "event": event,
        'events': events,
    }
    return render(request, "core/event_detail.html", context)
