from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets

from .models import *
from .forms import NewTaskForm, TaskModelFormset
from .serializers import TaskSerializer

from datetime import datetime, timedelta
import os

import logging

logger = logging.getLogger('django')
# Create your views here.

@login_required
def index(request):
    """
    Home page
    """
    tasks = Task.objects.filter(created_by=request.user, completed=False, start_date__gte=datetime.now().date()).order_by('start_date')
    past_tasks = Task.objects.filter(created_by=request.user, start_date__lt=datetime.now().date()) 

    return render(request, 'Tasks/index.html', {'tasks': tasks, 'past_tasks': past_tasks})

@login_required
def new_task(request):
    """
    View for creaing new tasks
    """
    template_name = 'Tasks/newtask.html'
    heading_message = 'Add New Tasks'
    if request.method == 'GET':
        # we don't want to display the already saved model instances
        formset = TaskModelFormset(queryset=Task.objects.none())
    elif request.method == 'POST':
        formset = TaskModelFormset(request.POST)
        if formset.is_valid():
            logger.info(len(formset))
            for form in formset:
                if form.is_valid():
                    if form.cleaned_data.get('title'):
                        task = form.save(commit=False)
                        task.created_by = request.user
                        task.finish_date = task.start_date + timedelta(days=10)
                        task.save()
                        logger.info(task)
                else:
                    logger.error("Form is invalid! %s" % form)
            messages.info(request, 'Task(-s) created by {0}.'.format(request.user))
            return redirect('Tasks:home')
    return render(request, template_name, {
            'formset': formset,
            'heading': heading_message,
        })

def temp(request):
    template_name = 'Tasks/newtask.html'

    return redirect('Tasks:home')

@login_required
def task_management(request):
    """
    View for creaing new tasks
    """
    tasks = Task.objects.filter(created_by=request.user, completed=False, start_date__gte=datetime.now().date()).order_by('start_date')

    if request.method == "POST":
        logger.info(request.POST)
        ids = request.POST.getlist('complete', '')
        for task_id in ids:        
            if task_id != '':
                task = Task.objects.get(task_id=task_id)
                task.completed = True
                task.save()



    return render(request, 'Tasks/manage.html', {'tasks': tasks})

@login_required
def tasks(request, task_type='all'):
    """
    Tasks list by type
    """

    if task_type == 'past':
        tasks = Task.objects.filter(created_by=request.user, start_date__lt=datetime.now().date())
    elif task_type == 'active':
        tasks = Task.objects.filter(created_by=request.user, completed=False, start_date__gte=datetime.now().date()).order_by('start_date')
    elif task_type == 'missed':
        tasks = Task.objects.filter(created_by=request.user, start_date__lt=datetime.now().date(), completed=False)
    else:
        tasks = Task.objects.filter(created_by=request.user)

    return render(request, 'Tasks/tasks.html', {'tasks': tasks, 'task_type': task_type})


@login_required
def task(request, task_id):
    """
    Individual task page
    """
    task = Task.objects.get(task_id=task_id)

    return render(request, 'Tasks/task-detail.html', {'task': task})


class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    queryset = Task.objects.all().order_by('-start_date')
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()


