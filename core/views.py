from django.shortcuts import render, get_object_or_404
from .models import Officer, Event

def index(request):
    leadership = Officer.objects.all()
    events = Event.objects.all()
    print(leadership)
    context = {
        'leadership' : leadership,
        'events' : events,
    }
    return render(request, "core/index.html", context)

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    events = Event.objects.all()
    context = {
        "event": event,
        'events' : events,
    }
    return render(request, "core/event_detail.html", context)
