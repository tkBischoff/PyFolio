from django.shortcuts import render
from django.http import Http404

# Create your views here.

def home(request):
    return render(request, 'home.html')

def browse(request):
    return render(request, 'browse.html')
