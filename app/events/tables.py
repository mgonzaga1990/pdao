import django_tables2 as tables
from .models import *

class DayActivityTable(tables.Table):
    class Meta:
        model = Event
        sequence = ('id','day','name','start_time','end_time')
        exclude = ("notes", )
        attrs = {"width": "100%"}

    action = tables.TemplateColumn('<a class="button" href="{{record.get_absolute_url}}">Update</a>&nbsp;' + 
                                   '<a class="button" href="/events/attendees/{{record.id}}">Attendees</a>')

class EventAttendeesTable(tables.Table):
    class Meta:
        model = EventAttendees
        fields = ('id','person','added_by')                                
        attrs = {"width": "100%"}

    action = tables.TemplateColumn('<a class="button" href="">Remove</a>&nbsp;')        