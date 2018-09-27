from django.shortcuts import render
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers

import json

from .forms import NewCountdownForm, CountdownModelForm
from .models import Countdown

import logging

logger = logging.getLogger('django')

def index(request):
    # Home page view: list of countdowns and a form to create a new one

    if request.method == 'POST':
        form = CountdownModelForm(request.POST)
        if form.is_valid():
            logger.info("form is valid")
            countdown = form.save(commit=False)
            countdown.created_by = request.user
            countdown.save()
    else:
        form = CountdownModelForm()
    countdowns = Countdown.objects.all()
    return render(request, 'home.html', {'form': form, 'countdowns': countdowns})

def countdown(request, delta=10):
    pk = "6d81ec95-9bcc-4bac-8398-ed0160441ba1"
    utc_offset = timedelta(hours=3)
    count_to = timezone.now() + timedelta(hours=10) #timezone
    count_to = datetime.now() + utc_offset #local
    count_to = datetime.now() + utc_offset + timedelta(minutes=delta) # actual countdown
    count_to = count_to.strftime("%b %d,  %Y %H:%M:%S")
    return render(request, 'countdown.html', {'count_to': count_to, "pk": pk})

def countdown_detail(request, pk):
    # Coundown by primary key
    utc_offset = timedelta(hours=3)
    c_pk = "fb3b96ae-38c2-42b1-a8ca-7ab63af5b061"
    count_to = datetime.now() + utc_offset + timedelta(minutes=10) # actual countdown
    count_to = count_to.strftime("%b %d,  %Y %H:%M:%S")
    countdown = Countdown.objects.get(countdown_id=pk)

    return render(request, 'countdown.html', {'count_to': count_to, "pk": pk, "countdown": countdown})
def send_countdown(request, cd_id):
    """
    Return countdown in json-format
    """

    countdown = Countdown.objects.get(countdown_id=cd_id)
    serialized_countdown = json.loads(serializers.serialize('json', [countdown, ]))
    #serialized_countdown[0]['fields']['countdown_to'] = "Jan 5, 2019 15:37:25"

    return JsonResponse(serialized_countdown, safe=False)