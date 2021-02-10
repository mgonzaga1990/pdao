from django.shortcuts import render
from .models import Event,EventAttendees
from .tables import *
from user.models import User

import datetime

def fetch_day_events(request,day,month,year):
    x = datetime.datetime(int(year), int(month), int(day))
    current_user = User.objects.get(id=request.user.id)

    if request.user.is_superuser:
        events = Event.objects.filter(day=x)
    else:
        events = Event.objects.filter(day=x,municipalities__in=current_user.municipalities.all())
    
    table = DayActivityTable(events)
    table.paginate(page=request.GET.get("page", 1), per_page=50)

    return render(request, 'day_events_list.html',{'table' : table})

def fetch_person_events(request,person_id):
    return render(request, 'person_events_list.html')

def fetch_attendees(request,event_id):
    event=Event.objects.get(id=event_id)
    attendees=EventAttendees.objects.filter(event=event)
    
    table = EventAttendeesTable(attendees)
    table.paginate(page=request.GET.get("page",1),per_page=50)

    return render(request,'event_attendees.html',{'table':table,'event':event})