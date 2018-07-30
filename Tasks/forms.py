from django import forms
from django.db.models import Q
from .models import Task

class DateInput(forms.DateInput):
    input_type = 'date'

class NewTaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'start_date']
        widgets = {
            'made_on': DateInput(),
        }