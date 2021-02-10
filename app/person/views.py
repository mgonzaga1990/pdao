from django.shortcuts import render
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse

from address.models import *

def fetch_brgy(request,municipal_id):
    # municipal_id = request.GET.get('municipal_id', None)
    municipal = Municipality.objects.get(id=municipal_id)
    brgy = Barangy.objects.filter(municipality=municipal)
    data = serializers.serialize("json", brgy)
    return HttpResponse(data, content_type='application/json')
    