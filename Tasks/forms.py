from django import forms
from django.forms import formset_factory
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

from django.forms import modelformset_factory

TaskModelFormset = modelformset_factory(
    Task,
    fields=['title', 'description', 'start_date', ],
    extra=1,
    widgets={'title': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Task Name here'
        }),
        'start_date': DateInput(),
    }
)