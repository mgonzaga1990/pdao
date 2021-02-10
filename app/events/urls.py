from django.conf.urls import url
from django.urls import path

from .views import *

urlpatterns = [
    path('get/<day>/<month>/<year>', fetch_day_events),

    path('all/<person_id>', fetch_person_events,name="activity"),

    path('attendees/<event_id>',fetch_attendees)
]
