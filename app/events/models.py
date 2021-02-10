from address.models import Municipality
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from person.models import *
from user.models import User

# from django.contrib.auth.models import User

# Create your models here.
# from __future__ import unicode_literals
 
class Event(models.Model):
    day = models.DateField(u'Day of the event', help_text=u'Day of the event')
    name = models.CharField(u'Event',max_length=15,help_text=u'Name of the Event')
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time')
    end_time = models.TimeField(u'End time', help_text=u'End time')
    notes = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)
    municipalities = models.ManyToManyField(Municipality)
    # created_by = models.ForeignKey(User,on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = u'Calendar'
        verbose_name_plural = u'Calendar'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        url = reverse('admin:%s_%s_change' % (self._meta.app_label, self._meta.model_name), args=[self.id])
        return url
        # return u'<a href="%s">%s</a>' % (url, str(self.name))    

class EventAttendees(models.Model):
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    person = models.ManyToManyField(Person)
    added_by = models.ForeignKey(User,on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'Event Attendees'
        verbose_name_plural = u'Attendees'
