from django import forms
from django.forms import formset_factory
from django.db.models import Q
from .models import Countdown

class DateInput(forms.DateTimeInput):
    input_type = 'datetime-local'

class NewCountdownForm(forms.Form):
    title= forms.CharField(max_length=100)
    countdown_to_date = forms.SplitDateTimeField(widget=DateInput())
    countdown_to_time_value = forms.CharField(max_length=5)
    countdown_to_time_type = forms.ChoiceField(choices=((1, 'minute(-s)'), (2, 'hour(-s)'), (3, 'day(-s)'), (4, 'month(-s)'), (5, 'year(-s)')))

