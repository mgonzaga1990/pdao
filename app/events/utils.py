from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
import datetime
from .models import Event


class EventCalendar(HTMLCalendar):
    def __init__(self, municipalities,is_super_user,events=None):
        super(EventCalendar, self).__init__()
        self.events = events
        self.municipalities = municipalities
        self.is_super_user = is_super_user

    def formatday(self, day, weekday, events,themonth,theyear):
        """
        Return a day as a table cell.
        """
        events_from_day = events.filter(day__day=day)
        counter = 0
        for event in events_from_day:
            counter+=1
        label = "<a href='/events/get/" + str(day) + "/" + str(themonth) + "/" + str(theyear) +"'><b>" + str(counter) + " Event(s)</b></a>"
        events_html = "<div style='padding:20px;background-color:#f0f0f5'>" + label if counter >0 else "" + "</div>"
        

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)

    def formatweek(self, theweek, events,themonth,theyear):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events,themonth,theyear) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """

        if self.is_super_user:
            events = Event.objects.filter(day__month=themonth)
        else:
            events = Event.objects.filter(day__month=themonth,municipalities__in=[u.pk for u in self.municipalities])

        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" style="width:100%" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events,themonth,theyear))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)