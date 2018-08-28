from django.shortcuts import render

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