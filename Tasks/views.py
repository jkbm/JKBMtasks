from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import viewsets
from django.views.generic import TemplateView, View

from .models import *
from .forms import NewTaskForm, TaskModelFormset, NewNoteForm

#DRF portion of imports
from rest_framework import status, renderers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
from rest_framework import generics
from .serializers import TaskSerializer, StandardTaskSerializer


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

@login_required
def notes(request):
    """
    List notes view
    """

    notes = Note.objects.filter(created_by=request.user)

    return render(request, 'Notes/notes.html', {'notes': notes})

@login_required
def note(reqest, note_id):
    """
    Note detail view
    """

    note = Note.objects.get(note_id=note_id)

    return render(reqest, 'Notes/note-detail.html', {'note': note})

@login_required
def new_note(request):
    """
    View for creating new notes
    """

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewNoteForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            logger.info("form is valid")
            note = form.save(commit=False)
            note.created_by = request.user
            note.save()

            messages.info(request, 'Note(-s) created by {0}.'.format(request.user))
            return redirect('/')
        else:
            logger.error("form is invalid")
            messages.error(request, 'FORM INVALID')
            return redirect('Tasks:new_note')

    else:
        form = NewNoteForm()

    return render(request, 'Notes/newnote.html', {'form': form})

def temp(request):
    template_name = 'Tasks/temp.html'
    context = {

    }
    return render(request, template_name)
    #return redirect('Tasks:home')

def temp_data(request):
    task_num = len(Task.objects.all())

    return JsonResponse({'tasks':task_num})

@login_required
def task_management(request):
    """
    View for creaing new tasks
    """
    tasks = Task.objects.filter(created_by=request.user, completed=False, start_date__gte=datetime.now().date()).order_by('start_date')

    if request.method == "POST":
        logger.info(request.POST)
        ids_complete = request.POST.getlist('complete', '')
        for task_id in ids_complete:        
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

@login_required
def task_delete(request, task_id):
    task = Task.objects.get(task_id=task_id)
    task.delete()
    messages.info(request, 'Task was deleted.')
    #redirect to prev. page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class TaskViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows tasks to be viewed or edited.
    """
    queryset = Task.objects.all().order_by('-start_date')
    serializer_class = TaskSerializer
    renderer_classes = [renderers.JSONRenderer]

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()

class TaskList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):

    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer