from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def home(request):
    return render(request, 'home.html')

def login(request):
    return render(request, 'login.html')

def index(request):
    string = u"hhhhhhhhhhh"
    return render(request, 'index.html', {'string': string})

