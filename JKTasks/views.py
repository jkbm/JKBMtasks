from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)
# Create your views here.

def index(request):
    """
    Home page view
    """
    
    return render(request, 'JKTasks/index.html')
