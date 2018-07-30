from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .models import *
from .forms import NewTaskForm

from datetime import datetime

import logging

logger = logging.getLogger(__name__)
# Create your views here.

def index(request):

    tasks = Task.objects.filter(created_by=request.user, completed=False, start_date__gte=datetime.now().date()).order_by('start_date')
    past_tasks = Task.objects.filter(created_by=request.user, start_date__lt=datetime.now().date()) 

    return render(request, 'Tasks/index.html', {'tasks': tasks, 'past_tasks': past_tasks})

def new_task(request):
    """
    View for creaing new tasks
    """

    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.finish_date = task.start_date
            logger.info("The value of user is %s", task.created_by)
            task.save()
            if 'create' in request.POST:
                messages.info(request, 'Task(-s) created by {0}.'.format(request.user))
                return redirect('Tasks:home')
    else:
        form = NewTaskForm()

    return render(request, 'Tasks/newtask.html', {'form': form,})

def tasks(request, task_type='all'):

    if task_type == 'past':
        tasks = Task.objects.filter(created_by=request.user, start_date__lt=datetime.now().date())
    elif task_type == 'active':
        tasks = Task.objects.filter(created_by=request.user, completed=False, start_date__gte=datetime.now().date()).order_by('start_date')
    elif task_type == 'missed':
        tasks = Task.objects.filter(created_by=request.user, start_date__lt=datetime.now().date(), completed=False)
    else:
        tasks = Task.objects.filter(created_by=request.user)

    return render(request, 'Tasks/tasks.html', {'tasks': tasks, 'task_type': task_type})

def task(request, task_id):
    """
    Individual task page
    """
    task = Task.objects.get(task_id=task_id)

    return render(request, 'Tasks/task-detail.html', {'task': task})
