from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .email_utils import send_contact_notification
from .forms import ContactMessageForm
from .models import Event, GalleryImage, Officer

def index(request):
    leadership = Officer.objects.all()
    homepage_events = list(Event.objects.order_by("date", "time")[:3])
    has_full_events = Event.objects.count() > len(homepage_events)
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
                send_contact_notification(contact_message)
                messages.success(
                    request,
                    f"Thanks for reaching out, {contact_message.first_name}! Your message has been sent to the club.",
                )
            except Exception as e:
                print("EMAIL ERROR:", str(e))  # 👈 this will show in Render logs
                messages.warning(
                    request,
                    "Your message was saved, but the email notification could not be sent right now.",
                )
            return redirect(f"{reverse('index')}?message=sent")
    else:
        form = ContactMessageForm()

    context = {
        'leadership': leadership,
        'events': homepage_events,
        "has_full_events": has_full_events,
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


def event_list(request):
    events = Event.objects.order_by("date", "time")
    context = {
        "events": events,
    }
    return render(request, "core/event_list.html", context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    events = Event.objects.order_by("date", "time")
    context = {
        "event": event,
        'events': events,
    }
    return render(request, "core/event_detail.html", context)
