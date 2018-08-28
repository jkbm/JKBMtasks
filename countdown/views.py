from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta

# Create your views here.
from .forms import NewCountdownForm

def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            pass  # does nothing, just trigger the validation
    else:
        form = NewCountdownForm()
    return render(request, 'home.html', {'form': form})

def countdown(request):
    utc_offset = timedelta(hours=3)
    count_to = timezone.now() + timedelta(hours=10) #timezone
    count_to = datetime.now() + utc_offset + timedelta(minutes=5) #local
    count_to = count_to.strftime("%b %d,  %Y %H:%M")
    return render(request, 'countdown.html', {'count_to': count_to})