import calendar
import datetime

from django.contrib import admin

from .models import *
from .utils import EventCalendar
from django.utils.safestring import mark_safe
from calendar import HTMLCalendar
from django.contrib.admin import DateFieldListFilter
from django import forms
from user.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple
from address.models import Municipality

@admin.register(EventAttendees)
class EventAttendeesAdmin(admin.ModelAdmin):
    exclude = ('added_by',)
    list_display = ('id','event','added_by')
    filter_horizontal = ('person',)
    
    def save_model(self,request,obj,form,change):
        obj.added_by = request.user
        super().save_model(request,obj,form,change)
        
    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

@admin.register(Event) 
class EventAdmin(admin.ModelAdmin):
    change_list_template = 'event_list.html'
    filter_horizontal = ('municipalities',)

    view_on_site = False

    def get_municipalities_qs(self,request):
        user = User.objects.get(id=request.user.id)
        qs = Municipality.objects.filter(pk__in=[u.pk for u in user.municipalities.all()])
        return qs

    def get_form(self, request,obj=None, **kwargs):
        form = super(EventAdmin, self).get_form(request, **kwargs)
        # form.current_user = request.user
        if request.user.is_superuser:
            pass
        else:
            qs = self.get_municipalities_qs(request)           
            form.base_fields['municipalities'] = forms.ModelMultipleChoiceField(queryset=qs,widget=FilteredSelectMultiple('Municipalities',is_stacked=False))
        
        return form

    # view events based on user's region(municipality)
    def changelist_view(self, request, extra_context=None):
        after_day = request.GET.get('day__gte', None)
        extra_context = extra_context or {}

        if not after_day:
            d = datetime.date.today()
        else:
            try:
                split_after_day = after_day.split('-')
                d = datetime.date(year=int(split_after_day[0]), month=int(split_after_day[1]), day=1)
            except:
                d = datetime.date.today()
      
        previous_month = datetime.date(year=d.year, month=d.month, day=1)  # find first day of current month
        previous_month = previous_month - datetime.timedelta(days=1)  # backs up a single day
        previous_month = datetime.date(year=previous_month.year, month=previous_month.month,
                                       day=1)  # find first day of previous month

        last_day = calendar.monthrange(d.year, d.month)
        next_month = datetime.date(year=d.year, month=d.month, day=last_day[1])  # find last day of current month
        next_month = next_month + datetime.timedelta(days=1)  # forward a single day
        next_month = datetime.date(year=next_month.year, month=next_month.month,
                                   day=1)  # find first day of next month

        extra_context['previous_month'] = reverse('admin:events_event_changelist') + '?day__gte=' + str(
            previous_month)
        extra_context['next_month'] = reverse('admin:events_event_changelist') + '?day__gte=' + str(next_month)
        extra_context['title'] = 'Monthly Event'

        municipalities = self.get_municipalities_qs(request)
        cal = EventCalendar(municipalities,request.user.is_superuser)
        html_calendar = cal.formatmonth(d.year, d.month, withyear=True)
        html_calendar = html_calendar.replace('<td ', '<td  width="150" height="150"')
        extra_context['calendar'] = mark_safe(html_calendar)
        return super(EventAdmin, self).changelist_view(request, extra_context)