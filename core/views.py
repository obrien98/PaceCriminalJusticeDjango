from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import ContactMessageForm
from .models import Event, Officer

def index(request):
    leadership = Officer.objects.all()
    events = Event.objects.all()

    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contact_message = form.save()
            send_mail(
                subject=f"CJS Contact Form: {contact_message.subject}",
                message=(
                    f"Name: {contact_message.name}\n"
                    f"Email: {contact_message.email}\n\n"
                    f"{contact_message.message}"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                fail_silently=True,
            )
            messages.success(
                request,
                "Thanks for reaching out. Your message has been sent to the club.",
            )
            return redirect(f"{reverse('index')}?message=sent")
    else:
        form = ContactMessageForm()

    context = {
        'leadership': leadership,
        'events': events,
        "contact_form": form,
    }
    return render(request, "core/index.html", context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    events = Event.objects.all()
    context = {
        "event": event,
        'events': events,
    }
    return render(request, "core/event_detail.html", context)
