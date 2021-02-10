from django import forms
from .models import *
from disability.models import *
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib import admin
from django.forms import modelformset_factory


class EvaluationForm(forms.Form):
    disabilities = forms.ModelChoiceField(required=True, queryset=Disability.objects.all())


class DisabilityForm(forms.Form):
    disabilities = forms.ModelChoiceField(required=True, queryset=Disability.objects.all())
