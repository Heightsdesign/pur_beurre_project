from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    message = "you're at the users index !"
    return HttpResponse(message)
