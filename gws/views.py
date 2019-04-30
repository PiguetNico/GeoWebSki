from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("Hello ! :)")

def list(request):

    return HttpResponse("This page should display the list of slopes...")
