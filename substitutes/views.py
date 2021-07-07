from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    message = "You're at the substitutes index !"
    return HttpResponse(message)

def search(request):
    obj = str(request.GET)
    query = request.GET['query']
    message = "propriété GET : {} et requête : {}".format(obj, query)
    return HttpResponse(message)

def product_detail(request, product_id):
    id = int(product_id) # make sure we have an integer.
    message = "L'id du produit est : {}".format(id)
    return HttpResponse(message)
